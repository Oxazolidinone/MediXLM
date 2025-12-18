"""Environmental Law Knowledge entity for Knowledge Graph."""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any, List
from uuid import UUID, uuid4


class KnowledgeType(str, Enum):
    KHAI_NIEM = "KhaiNiem"
    DOI_TUONG = "DoiTuong"
    CO_QUAN = "CoQuan"
    HANH_VI = "HanhVi"
    QUYEN_NGHIA_VU = "QuyenNghiaVu"
    TRACH_NHIEM = "TrachNhiem"
    NHOM_DU_AN = "NhomDuAn"
    GIAI_DOAN = "GiaiDoan"
    BUOC_QUY_TRINH = "BuocQuyTrinh"
    KET_QUA = "KetQua"


@dataclass
class EnvLawKnowledge:
    id: str  # Can be Neo4j internal ID or custom ID (e.g. KN001)
    name: str # Ten
    knowledge_type: KnowledgeType # Label
    description: Optional[str] = None # Mo ta / Noi dung
    properties: Dict[str, Any] = None
    embeddings: Optional[List[float]] = None
    source: Optional[str] = None # Dieu khoan reference

    def __post_init__(self):
        if self.properties is None:
            self.properties = {}

    @staticmethod
    def create(
        id: str,
        name: str,
        knowledge_type: KnowledgeType,
        description: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None,
        source: Optional[str] = None,
    ) -> "EnvLawKnowledge":
        return EnvLawKnowledge(
            id=id,
            name=name,
            knowledge_type=knowledge_type,
            description=description,
            properties=properties or {},
            source=source,
        )
