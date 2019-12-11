"""Test the main module."""
from accountlinks_generator.accountlinks_generator import (
    yaml_loader,
    get_all_prefixes,
    get_account_number,
    get_all_roles_within_environment,
    get_all_roles,
    get_environments_with_common_prefix,
    role_formatter,
    generate_account_links,
    make_table_header,
    make_table_border,
    make_table_body,
    make_entire_table,
    generate_entire_document,
)


mock_config = "files/mock_config.yaml"
small_mock_config = "files/small_mock_config.yaml"


def test_get_all_prefixes():
    data = yaml_loader(mock_config)
    groups = data.get("common")
    assert get_all_prefixes(groups) == ["auth", "sandbox", "test"]
    assert get_all_prefixes(groups) != ["auth", "auth", "sandbox", "test"]


def test_get_account_number():
    data = yaml_loader(mock_config)
    groups = data.get("common")
    assert get_account_number("sandbox", groups) == 12345
    assert get_account_number("auth-test", groups) == 21212
    assert get_account_number("auth", groups) != 21212


def test_get_all_roles_within_environment():
    data = yaml_loader(mock_config)
    groups = data.get("common")
    assert get_all_roles_within_environment("sandbox", groups) == (
        ["RoleAdministrator", "RoleSandboxEngineer", "RoleSandboxViewer"]
    )


def test_get_all_roles():
    data = yaml_loader(mock_config)
    groups = data.get("common")
    assert get_all_roles("auth", groups) == (
        [
            "RoleAdministrator",
            "RoleEncryption",
            "RoleIRO",
            "RolePO",
            "RoleSecAdministrator",
            "RoleTest",
        ]
    )


def test_get_environments_with_common_prefix():
    data = yaml_loader(mock_config)
    groups = data.get("common")
    assert get_environments_with_common_prefix("auth", groups) == ["auth", "auth-test"]


def test_role_formatter():
    assert role_formatter("RoleTestRole") == "TestRole"
    assert role_formatter("RoleSandboxViewer") == "SandboxViewer"


def test_genenerate_account_links():
    data = yaml_loader(mock_config)
    groups = data.get("common")
    assert (
        generate_account_links("test-base", "RoleBEngineer", groups)
        == "https://signin.aws.amazon.com/switchrole?account=76543&roleName=RoleBEngineer&displayName=RoleBEngineer"
    )


def test_make_table_header():
    data = yaml_loader(mock_config)
    groups = data.get("common")
    assert (
        make_table_header("auth", groups)
        == "| Environment | Account No. | RoleAdministrator | RoleEncryption | RoleIRO | RolePO | RoleSecAdministrator | RoleTest |"
    )


def test_make_table_border():
    data = yaml_loader(mock_config)
    groups = data.get("common")
    assert make_table_border("auth", groups) == "|---|---|---|---|---|---|---|---|"
    assert make_table_border("sandbox", groups) == "|---|---|---|---|---|"


def test_make_table_body():
    data = yaml_loader(mock_config)
    groups = data.get("common")

    assert (
        make_table_body("test-base", "test", groups)
        == "| test-base | 76543 | [BEngineer](https://signin.aws.amazon.com/switchrole?account=76543&roleName=RoleBEngineer&displayName=RoleBEngineer) |"
    )


def test_make_entire_table():
    data = yaml_loader(small_mock_config)
    groups = data.get("common")
    assert (
        make_entire_table("firsttest", groups)
        == "| Environment | Account No. | RoleTest |\n|---|---|---|\n| firsttest | 12345 | [Test](https://signin.aws.amazon.com/switchrole?account=12345&roleName=RoleTest&displayName=RoleTest) |\n"
    )


def test_generate_entire_document():
    data = yaml_loader(small_mock_config)
    groups = data.get("common")
    intro = "None"
    outro = "None"
    assert generate_entire_document(groups, intro, outro) is None
