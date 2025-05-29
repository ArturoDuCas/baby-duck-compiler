from dataclasses import dataclass
from src.virtual_machine.frame_resources import FrameResources
from src.semantic.function_dir import FunctionDir, SignatureType
from src.errors.internal_compiler_error.compiler_bug import CompilerBug


@dataclass
class FunctionRuntimeInfo:
    frame_resources: FrameResources
    signature: SignatureType
    initial_quad_index: int

class FunctionRuntimeInfoMap:
    """
    Maps function names to their runtime information.
    """
    
    def __init__(self, function_dir: FunctionDir):
        self._map: dict[str, FunctionRuntimeInfo] = {}
        for name, func in function_dir.get_function_dir().items():
            if func.frame_resources is None:
                raise CompilerBug(f"Function '{name}' does not have frame resources defined.")
            self._map[name] = FunctionRuntimeInfo(
                frame_resources=func.frame_resources,
                signature=func.signature,
                initial_quad_index=func.initial_quad_index
            )


    def get_function_runtime_info(self, name: str) -> FunctionRuntimeInfo:
        """
        Returns the runtime information for a function by its name.
        """
        if name not in self._map:
            raise CompilerBug(f"Function '{name}' not found in runtime info map.")
        
        return self._map[name]


    def get_frame_resources(self, name: str) -> FrameResources:
        """
        Returns the frame resources for a function by its name.
        """
        return self.get_function_runtime_info(name).frame_resources


    def get_signature(self, name: str) -> SignatureType:
        """
        Returns the signature for a function by its name.
        """
        return self.get_function_runtime_info(name).signature


    def get_initial_quad_index(self, name: str) -> int:
        """
        Returns the initial quadruple index for a function by its name.
        """
        return self.get_function_runtime_info(name).initial_quad_index