## Copyright 2015 Ray Holder
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
## http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.

import csv
import json
import sys
from threading import local

import click
from joblib import Parallel, delayed
from pyelasticsearch import ElasticSearch
from pyelasticsearch import bulk_chunks
from pyelasticsearch import ElasticHttpNotFoundError
from pyelasticsearch import IndexAlreadyExistsError
from retrying import retry


__version__ = '1.0.1'
thread_local = local()


def echo(message, quiet):
    """
    Print the given message to standard out via click unless quiet is True.

    :param message: the message to print out to the console
    :param quiet: don't print the message when this is True
    """
    if not quiet:
        click.echo(message)


def documents_from_file(es, filename, quiet):
    """
    Return a generator for pulling rows from a given delimited file.

    :param es: an ElasticSearch client
    :param filename: the name of the file to read from or '-' if stdin
    :param delimiter: the delimiter to use
    :param quiet: don't output anything to the console when this is True
    :return: generator returning document-indexing operations
    """
    def all_docs():
        with open(filename, 'rb') if filename != '-' else sys.stdin as doc_file:

            count = 0
            docs = json.load(doc_file)
            for doc in docs:
                count += 1
                if count % 10000 == 0:
                    echo('Sent documents: ' + str(count), quiet)
                yield es.index_op(doc)

    return all_docs


@retry(wait_exponential_multiplier=1000, wait_exponential_max=10000, stop_max_attempt_number=10)
def local_bulk(host, index_name, doc_type, chunk):
    """
    Bulk upload the given chunk, creating a thread local ElasticSearch instance
    for the target host if one does not already exist. Retry this function at
    least 10 times with exponential backoff.

    :param host: the target Elasticsearch host
    :param index_name: the index name
    :param doc_type: the document type
    :param chunk: the chunk of documents to bulk upload
    """
    if not hasattr(thread_local, 'es'):
        thread_local.es = ElasticSearch(host)

    thread_local.es.bulk(chunk, index=index_name, doc_type=doc_type)


def perform_bulk_index(host, index_name, doc_type, doc_fetch, docs_per_chunk, bytes_per_chunk, parallel):
    """
    Chunk up documents and send them to Elasticsearch in bulk.

    :param host: the target Elasticsearch host
    :param index_name: the target index name
    :param doc_type: the target document type
    :param doc_fetch: a function to call to fetch documents
    :param docs_per_chunk: the number of documents per chunk to upload
    :param bytes_per_chunk: the max bytes per chunk to upload
    :param parallel: the number of bulk uploads to do at the same time
    """
    Parallel(n_jobs=parallel)(
        delayed(local_bulk)(host, index_name, doc_type, chunk)
        for chunk in bulk_chunks(doc_fetch(),
                                 docs_per_chunk=docs_per_chunk,
                                 bytes_per_chunk=bytes_per_chunk))



@click.command()
@click.option('--index-name', required=True,
              help='Index name to load data into         ')
@click.option('--doc-type', required=True,
              help='The document type (like user_records)')
@click.option('--import-file', required=True,
              help='File to import (or \'-\' for stdin)    ')
@click.option('--mapping-file', required=False,
              help='JSON mapping file for index')
@click.option('--host', default='http://127.0.0.1:9200/', required=False,
              help='The Elasticsearch host (http://127.0.0.1:9200/)')
@click.option('--docs-per-chunk', default=5000, required=False,
              help='The documents per chunk to upload (5000)')
@click.option('--bytes-per-chunk', default=100000, required=False,
              help='The bytes per chunk to upload (100000)')
@click.option('--parallel', default=1, required=False,
              help='Parallel uploads to send at once, defaults to 1')
@click.option('--delete-index', is_flag=True, required=False,
              help='Delete existing index if it exists')
@click.option('--quiet', is_flag=True, required=False,
              help='Minimize console output')
@click.version_option(version=__version__, )
def cli(index_name, delete_index, mapping_file, doc_type, import_file,
        host, docs_per_chunk, bytes_per_chunk, parallel, quiet):
    """
    Bulk import a delimited file into a target Elasticsearch instance. Common
    delimited files include things like CSV and TSV.

    \b
    Load a CSV file:
      csv2es --index-name potatoes --doc-type potato --import-file potatoes.csv
    \b
    For a TSV file, note the tab delimiter option
      csv2es --index-name tomatoes --doc-type tomato --import-file tomatoes.tsv --tab
    \b
    For a nifty pipe-delimited file (delimiters must be one character):
      csv2es --index-name pipes --doc-type pipe --import-file pipes.psv --delimiter '|'

    """

    echo('Using host: ' + host, quiet)
    es = ElasticSearch(host)

    if delete_index:
        try:
            es.delete_index(index_name)
            echo('Deleted: ' + index_name, quiet)
        except ElasticHttpNotFoundError:
            echo('Index ' + index_name + ' not found, nothing to delete', quiet)

    try:
        es.create_index(index_name)
        echo('Created new index: ' + index_name, quiet)
    except IndexAlreadyExistsError:
        echo('Index ' + index_name + ' already exists', quiet)

    echo('Using document type: ' + doc_type, quiet)
    if mapping_file:
        echo('Applying mapping from: ' + mapping_file, quiet)
        with open(mapping_file) as f:
            mapping = json.loads(f.read())
        es.put_mapping(index_name, doc_type, mapping)

    documents = documents_from_file(es, import_file, quiet)
    perform_bulk_index(host, index_name, doc_type, documents, docs_per_chunk, bytes_per_chunk, parallel)


if __name__ == "__main__":
    cli()
