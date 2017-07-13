import argparse
import hashlib
import os
import sys
import yaml

from datetime import datetime, timezone


# Don't add these keys to the output
STRIP_KEYS = ['agent', 'author_IP', 'date_gmt', 'type', 'user_id']

# Transform these keys to a new name
TRANSFORM_KEYS = {
    'ID': '_id',
    'author': 'name',
    'author_email': 'email',
    'author_url': 'url',
    'content': 'message',
}

# Skip comments containing these key value pairs
EXCLUDE_IF = {
    'type': 'pingback',
}


def wp2staticman(comments_file, post_file, output_dir):
    post_slugs = yaml.load(post_file)

    comments_in = yaml.load(comments_file)
    for comment_in in comments_in:
        comment_out = parse_comment(comment_in)
        if not comment_out:
            continue

        comment_dir = post_slugs[comment_out['post_ID']]
        out_dir = os.path.join(output_dir, comment_dir)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        timestamp = comment_out['date']
        out_file = os.path.join(out_dir, f"entry{timestamp}.yml")
        with open(out_file, 'w+') as entry_f:
            yaml.dump(comment_out, entry_f)


def parse_comment(comment_in):
    """
    Convert a single WordPress comment in dict format to a Staticman
    comment in dict format.
    """
    comment_out = {
        k.replace('comment_', '', 1): v for k, v in comment_in.items()}
    for k, v in EXCLUDE_IF.items():
        if k in comment_out and comment_out[k] == v:
            return None
    for k in STRIP_KEYS:
        comment_out.pop(k)
    for key, new_key in TRANSFORM_KEYS.items():
        v = comment_out.pop(key)
        comment_out[new_key] = v
    comment_out['date'] = convert_date(comment_out['date'])
    comment_out['email'] = convert_email(comment_out['email'])
    return comment_out


def convert_date(date_str):
    """ Convert date string in UTC to iso """
    naive = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    utc = naive.replace(tzinfo=timezone.utc)
    return int(utc.timestamp())


def convert_email(email):
    """ MD5 hash the email address """
    email = email.strip().encode('utf-8').lower()
    return hashlib.md5(email).hexdigest()


def parse_args(args):
    parser = argparse.ArgumentParser(
        description="Convert WordPress comments to Staticman comments.")
    parser.add_argument(
        'comments',
        help="WordPress comments file in yaml format"
    )
    parser.add_argument(
        "post_meta",
        help="WordPress post meta file in yaml format"
    )
    parser.add_argument(
        "output",
         help="Directory to output Postman formatted comments"
    )
    return parser.parse_args(args)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    with open(args.comments) as comments_f, open(args.post_meta) as posts_f:
        wp2staticman(comments_f, posts_f, args.output)
