import os
import pytest
import yaml

from testfixtures import TempDirectory

from wp2staticman import wp2staticman
from . import comments


@pytest.mark.parametrize("date_str,expected", [
    ("2017-06-10 18:09:00", 1497118140),
])
def test_convert_date(date_str, expected):
    assert expected == wp2staticman.convert_date(date_str)


@pytest.mark.parametrize("email,hashed", [
    (" MyEmailAddress@example.com ", "0bc83cb571cd1c50ba6f3e8a78ef1346"),
    ("MyEmailAddress@example.com", "0bc83cb571cd1c50ba6f3e8a78ef1346"),
    ("myemailaddress@example.com ", "0bc83cb571cd1c50ba6f3e8a78ef1346"),
])
def test_convert_email(email, hashed):
    assert hashed == wp2staticman.convert_email(email)


@pytest.mark.parametrize(
    "comment_in,comment_out",
    list(zip(comments.wp_comments, comments.staticman_comments))
)
def test_parse_comment(comment_in, comment_out):
    dict_in = yaml.load(comment_in)[0]
    dict_out = None
    if comment_out is not None:
        dict_out = yaml.load(comment_out)[0]
    assert dict_out == wp2staticman.parse_comment(dict_in)


def test_parse_args():
    comments_filename = 'comments_file.yml'
    post_meta_filename = 'post.yml'
    out_dir = '_posts/data'

    args = wp2staticman.parse_args([
        comments_filename,
        post_meta_filename,
        out_dir
    ])

    assert args.comments == comments_filename
    assert args.post_meta == post_meta_filename
    assert args.output == args.output


def test_wp2staticman():
    comment_yaml = comments.wp_comments[0]
    comment = yaml.load(comment_yaml)[0]
    comment_id = comment['comment_ID']
    comment_slug = 'test-slug'
    comments_f = (
        "---\n"
        f"{comment_yaml}"
    )
    post_f = (
        "---\n"
        f' {comment_id}: "{comment_slug}"'
    )
    print(comments_f)

    with TempDirectory() as d:
        wp2staticman.wp2staticman(comments_f, post_f, d.path)

        assert os.path.exists(os.path.join(d.path, comment_slug))


