from pydantic import BaseModel, ConfigDict


class FromAttributes:
    """
    A mixin that allows the model to be initialized from attributes.
    """

    model_config = ConfigDict(from_attributes=True)


class PatchModel(BaseModel):
    """
    A model that forces exclude None values from the model dump.

    NOTE: Use instead BaseModel if you want to exclude None values from the
    model dump.

    Example:
    ```
    class MyModel(PatchModel):
        name: str
        age: int | None = None
    ```
    """

    def model_dump(self, **kwargs):
        return super().model_dump(exclude_unset=True, **kwargs)
