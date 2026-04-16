from pathlib import Path
import subprocess
import shutil
from jinja2 import Environment, FileSystemLoader
import os
from collections.abc import Mapping


def create_folder(folder_path: str) -> Path:
    try:
        target_path = Path(folder_path).expanduser()
    except Exception as e:
        raise Exception(f"Invalid path: {folder_path}") from e

    if target_path.exists():
        if not target_path.is_dir():
            raise Exception(f"Path exists and is not a directory: {folder_path}")

        try:
            is_empty = not any(target_path.iterdir())
        except PermissionError as e:
            raise Exception(f"Permission denied: {folder_path}") from e

        if not is_empty:
            raise Exception(f"Directory is not empty: {folder_path}")

        print(f"Directory already exists and is empty: {folder_path}")
    else:
        parent = target_path.parent
        if not parent.exists():
            raise Exception(f"Parent directory does not exist: {parent}")
        if not parent.is_dir():
            raise Exception(f"Parent path exists and is not a directory: {parent}")

        try:
            target_path.mkdir(parents=False, exist_ok=False)
        except PermissionError as e:
            raise Exception(f"Permission denied: {folder_path}") from e
        except OSError as e:
            raise Exception(f"Failed to create directory: {folder_path}") from e

        print(f"Directory created: {folder_path}")

    return target_path


def create_template(
    target_path: Path,
    project_description: str,
    init_git: bool = True,
) -> None:
    """
    Copy template content to target path and render Jinja2 templates.

    Args:
        target_path: Path to the target directory where template will be created
        project_description: Project description used for template rendering

    Raises:
        Exception: If template source doesn't exist or operations fail
    """
    # Get the template source directory (relative to this package)
    template_source = Path(__file__).parent.parent / "template"

    if not template_source.exists():
        raise Exception(f"Template source not found: {template_source}")

    try:
        # 1. Copy all content from template/ to target_path
        for item in template_source.iterdir():
            src_item = template_source / item.name
            dst_item = target_path / item.name

            if src_item.is_dir():
                shutil.copytree(src_item, dst_item)
            else:
                shutil.copy2(src_item, dst_item)

        print(f"Template content copied to {target_path}")

        # 2. Process Jinja2 template files
        context = {
            "project_name": target_path.name,
            "project_description": project_description,
        }
        process_jinja_templates(target_path, context)
        if init_git:
            init_git_repository(target_path)
        print_next_steps(target_path.name)

    except Exception as e:
        raise Exception(f"Failed to create template: {str(e)}") from e


def init_git_repository(target_path: Path) -> None:
    try:
        subprocess.run(
            ["git", "init"],
            cwd=target_path,
            check=True,
            capture_output=True,
            text=True,
        )
        print(f"Initialized git repository in {target_path}")
    except FileNotFoundError as e:
        raise Exception("Git is not installed or not available in PATH") from e
    except subprocess.CalledProcessError as e:
        raise Exception(
            f"Failed to initialize git repository in {target_path}: {e.stderr.strip()}"
        ) from e


def print_next_steps(project_name: str) -> None:
    print(
        f"""
Your project "{project_name}" has been created successfully!

Next steps:

1. Change directory to the project root:

    $ cd {project_name}

2. Install tools
- justfile
- uv

3. Install dependencies:

    $ uv sync

4. Start developing your project!

    $ just dev
"""
    )


def process_jinja_templates(
    root_path: Path, context: Mapping[str, object] | None = None
) -> None:
    """
    Recursively process and render Jinja2 templates.

    Args:
        root_path: Root directory to process
        context: Dictionary of variables to pass to Jinja2 templates
    """
    if context is None:
        context = {}

    # Setup Jinja2 environment
    env = Environment(loader=FileSystemLoader(str(root_path)))

    # Recursively walk through all files
    for root, _, files in os.walk(root_path):
        root_dir = Path(root)

        for file in files:
            if file.endswith(".jinja"):
                file_path = root_dir / file

                try:
                    # Read and render the template
                    with open(file_path, "r", encoding="utf-8") as f:
                        template_content = f.read()

                    # Render template with context
                    template = env.from_string(template_content)
                    rendered_content = template.render(**context)

                    # Create new file without .jinja extension
                    new_file_path = root_dir / file[:-6]  # Remove .jinja

                    with open(new_file_path, "w", encoding="utf-8") as f:
                        f.write(rendered_content)

                    # Remove original .jinja file
                    file_path.unlink()

                    print(f"Rendered template: {new_file_path.relative_to(root_path)}")

                except Exception as e:
                    raise Exception(
                        f"Failed to process template {file_path}: {str(e)}"
                    ) from e

