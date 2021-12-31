from pathlib import Path
from tempfile import TemporaryDirectory

from py_executable_checklist.workflow import WorkflowBase
from slug import slug  # type: ignore


class CreateOutputFolder(WorkflowBase):
    """Create output folder using Post id in the temporary folder"""

    post_title: str

    def run(self, context: dict) -> None:
        blog_title_slug = slug(self.post_title)
        temp_folder = TemporaryDirectory()
        target_folder = Path(temp_folder.name) / blog_title_slug
        child_links_folder = target_folder / "links"
        thumbnails_folder = target_folder / "thumbnails"

        for f in [target_folder, child_links_folder, thumbnails_folder]:
            f.mkdir(parents=True, exist_ok=True)

        # output
        context["target_folder"] = target_folder
        context["child_links_folder"] = child_links_folder
        context["thumbnails_folder"] = thumbnails_folder


def workflow_steps() -> list:
    return [CreateOutputFolder]
