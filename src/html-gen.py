#!/usr/bin/python3
import datetime
import json
import os
import sys
import time


def main(json_data):
    assets_path = json_data['content-root']
    save_path = json_data['webserver-root']

    # Build pages
    for page in json_data['pages']:
        header = ''
        if 'header' in page['content']:
            items = sorted(page['content']['header'])
            # Sort JSON elements to prevent them from being inserted
            # in random order
            for item in items:
                file = os.path.normpath(os.path.join(assets_path,
                                        page['content']['header'][item]))
                print('HEADER: appending {}'.format(file))
                with open(file, 'r') as f:
                    header += f.read()
        timestamp = get_datetime_with_offset()
        header += '\n<!-- Generated on {} by David Lucadou\'s Python HTML Ge' \
                  'nerator\nhttps://github.com/davidlucadou/py-html-builder' \
                  ' -->\n'.format(timestamp)
        header += '<!DOCTYPE html>'
        header += '\n<html lang="{}">'.format(page['lang'])
        head = '\n<head>\n'
        if 'head' in page['content']:
            items = sorted(page['content']['head'])
            for item in items:
                file = os.path.normpath(os.path.join(assets_path,
                                                     page['content']['head']
                                                     [item]))
                print('HEAD: appending {}'.format(file))
                with open(file, 'r') as f:
                    head += f.read()
                    head += '\n'
        head += '</head>\n'

        if 'body-tag' in page['content']:
            # Use body-tag for ids and classes, i.e.:
            # <body id="my-body" class="body-darktheme">
            # should use:
            # "body-tag": "id=\"my-body\" class=\"body-darktheme\""
            body = '<body {}>\n' + page['content']['body-tag']
        else:
            body = '<body>\n'
        if 'body' in page['content']:
            items = sorted(page['content']['body'])
            for item in items:
                file = os.path.normpath(os.path.join(assets_path,
                                                     page['content']['body']
                                                     [item]))
                print('BODY: appending {}'.format(file))
                with open(file, 'r') as f:
                    body += f.read()
                    body += '\n'
        body += '</body>'
        body += '\n</html>'
        html = header + head + body
        file = os.path.normpath(os.path.join(save_path, page['path']))

        # Write file to disk
        with open(file, 'w') as f:
            f.write(html)
            print('Wrote to {}'.format(file))


def get_datetime_with_offset():
    epochtime = int(time.time())  # cast to int removes milliseconds
    utc_offset_seconds = (datetime.datetime.fromtimestamp(epochtime)
                          - datetime.datetime.utcfromtimestamp(epochtime))
    utc_offset_minutes = utc_offset_seconds / datetime.timedelta(minutes=1)
    utc_offset_hrs = utc_offset_minutes / 60

    # return as int if an hourly offset, float if partial hour offset
    # (GMT-5 looks better than GMT-5.0, but GMT+3.5 will be preserved)
    if utc_offset_hrs % 2 == 0:
        utc_offset_hrs = int(utc_offset_hrs)

    now = str(datetime.datetime.now())[:-7] + ' GMT' + str(utc_offset_hrs)
    return now


if __name__ == '__main__':
    input_file = sys.argv[1]
    with open(input_file, 'r') as f:
        data = f.read()
    json_data = json.loads(data)
    main(json_data)
