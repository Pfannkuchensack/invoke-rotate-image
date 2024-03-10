from typing import Literal
from PIL import Image


from invokeai.app.services.image_records.image_records_common import ImageCategory, ResourceOrigin
from invokeai.app.invocations.baseinvocation import (
    BaseInvocation,
    InputField,
    invocation,
    InvocationContext,
    WithMetadata,
    WithWorkflow,
)

from invokeai.app.invocations.primitives import (
    ImageField,
    ImageOutput
)

@invocation(
    "invoke_image_rotate",
    title="Image Rotate",
    tags=["image", "rotate"],
    category="image",
    version="1.0.0",
)
class RotateImageInvocation(BaseInvocation, WithMetadata, WithWorkflow):
    """Rotate an image by a given angle."""
    image: ImageField = InputField(default=None, description="Image to be rotated")
    rotate: int = InputField(default=180., description="The angle to rotate the image")

    def invoke(self, context: InvocationContext) -> ImageOutput:

        image = context.services.images.get_pil_image(self.image.image_name)

        image.rotate(self.rotate)

        image_dto = context.services.images.create(
            image=image,
            image_origin=ResourceOrigin.INTERNAL,
            image_category=ImageCategory.GENERAL,
            node_id=self.id,
            session_id=context.graph_execution_state_id,
            is_intermediate=self.is_intermediate,
            workflow=self.workflow,
        )

        return ImageOutput(
            image=ImageField(image_name=image_dto.image_name),
            width=image_dto.width,
            height=image_dto.height,
        )