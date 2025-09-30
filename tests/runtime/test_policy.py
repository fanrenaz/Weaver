from weaver.runtime.policy import MediationPolicy


def test_mediation_policy_system_prompt_contains_keywords():
    policy = MediationPolicy.default()
    prompt = policy.format_system_prompt()
    assert "财务" in prompt
    assert "核心" in prompt or "Core Principles" in prompt
    # Ensure principles were enumerated
    for p in policy.principles:
        assert p in prompt
