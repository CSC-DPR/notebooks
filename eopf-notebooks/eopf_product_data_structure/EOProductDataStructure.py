
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from eopf.product.core import EOVariable, EOGroup, EOProduct, MetaData
from typing import Any, Optional, Union
import xarray as xr
import numpy as np

from utils import create_data

class Builder(ABC):

    @abstractmethod
    def compute(self):
        """ """

@dataclass
class EOProductBuilder(Builder):
    name: str
    groups: list[EOGroup] = field(default_factory=list)
    coords: Optional[Union[EOGroup, "EOGroupBuilder"]] = None
    attrs:dict = field(default_factory=dict)
    metadatas: list[str] = field(default_factory=list)

    def compute(self):
        groups = map(lambda g: g.compute() if isinstance(g, EOGroupBuilder) else g, self.groups)
        coords = self.coords.compute() if isinstance(self.coords, EOGroupBuilder) else self.coords
        return EOProduct(self.name, coords, groups=groups, attrs=self.attrs, metadatas=map(MetaData, self.metadatas))


@dataclass
class EOGroupBuilder(Builder):
    name: str
    variables: list[EOVariable] =  field(default_factory=list)
    groups: list[EOGroup] = field(default_factory=list)
    attrs: dict = field(default_factory=dict)
    dims: list[str] = field(default_factory=list)
    coords: Optional[Union[EOGroup, "EOGroupBuilder"]] = None

    def compute(self):
        groups = map(lambda g: g.compute() if isinstance(g, EOGroupBuilder) else g, self.groups)
        variables = map(lambda v: v.compute() if isinstance(v, EOVariableBuilder) else v, self.variables)
        coords = self.coords.compute() if isinstance(self.coords, EOGroupBuilder) else self.coords
        dims = set(self.dims)
        return EOGroup(self.name, variables=variables, groups=groups, attrs=self.attrs, coords=coords, dims=dims)


DEFAULT_ATTRS = {
    attr: "TBD"
    for attr in ["long_name","standard_name","units","valid_max","valid_min","scale_factor","add_offset","_FillValue"]
}

@dataclass
class EOVariableBuilder(Builder):
    name: str
    data: Any = None
    attrs: dict = field(default_factory=dict)
    dims: list[str] = field(default_factory=list)
    dtype: Any = "float32"
    default_attrs: bool = False

    def compute(self):
        attrs = self.attrs if not self.default_attrs else DEFAULT_ATTRS
        try:
            dtype = np.dtype(self.dtype.strip())
        except Exception:
            dtype = np.float32
        dims = set(self.dims)
        return EOVariable(xr.DataArray(name=self.name, data=self.data or create_data(len(dims)), attrs=attrs, dims=dims).astype(dtype))
