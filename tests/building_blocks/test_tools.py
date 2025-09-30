from weaver.building_blocks.tools import reply_privately, post_to_shared


def test_reply_privately_echo():
    out = reply_privately.invoke({"recipient": "test_user", "content": "hello"})
    assert out == "[private -> test_user] hello"


def test_post_to_shared_echo():
    out = post_to_shared.invoke({"content": "broadcast msg"})
    assert out == "[shared] broadcast msg"
