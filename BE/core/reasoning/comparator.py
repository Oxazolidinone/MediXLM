# -*- coding: utf-8 -*-
"""
ReasonerComparator - Compares and synthesizes outputs from multiple reasoners.
Part of EnvLawReasoner multi-reasoner system.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from .reasoners.base_reasoner import ReasonerResult


@dataclass
class ComparisonReport:
    """Report comparing outputs from multiple reasoners."""
    
    # Summary stats
    total_reasoners: int = 0
    successful_reasoners: int = 0
    
    # Agreement analysis
    agreement_score: float = 0.0  # 0.0 - 1.0
    common_conclusions: List[str] = field(default_factory=list)
    conflicts: List[Dict[str, Any]] = field(default_factory=list)
    
    # Rankings
    ranked_results: List[Dict[str, Any]] = field(default_factory=list)
    best_reasoner: str = ""
    
    # Formatted output
    comparison_text: str = ""
    
    def to_dict(self) -> Dict:
        return {
            "total_reasoners": self.total_reasoners,
            "successful_reasoners": self.successful_reasoners,
            "agreement_score": self.agreement_score,
            "common_conclusions": self.common_conclusions,
            "conflicts": self.conflicts,
            "ranked_results": self.ranked_results,
            "best_reasoner": self.best_reasoner
        }


class ReasonerComparator:
    """
    Compares outputs from multiple reasoners.
    
    Features:
    - Calculate agreement score
    - Identify conflicts
    - Rank by confidence
    - Generate human-readable comparison
    """
    
    def compare(self, results: Dict[str, ReasonerResult]) -> ComparisonReport:
        """
        Compare results from multiple reasoners.
        
        Args:
            results: Dict mapping reasoner name to result
            
        Returns:
            ComparisonReport with analysis
        """
        report = ComparisonReport()
        
        if not results:
            return report
        
        report.total_reasoners = len(results)
        
        # Filter successful results
        successful = {
            name: res for name, res in results.items()
            if res.success
        }
        report.successful_reasoners = len(successful)
        
        if not successful:
            report.comparison_text = "Không có reasoner nào thực hiện thành công."
            return report
        
        # 1. Calculate agreement score
        all_conclusions = []
        for res in successful.values():
            all_conclusions.extend(res.conclusions)
        
        # Find common conclusions (appears in multiple reasoners)
        conclusion_counts = {}
        for c in all_conclusions:
            normalized = c.lower().strip()
            conclusion_counts[normalized] = conclusion_counts.get(normalized, 0) + 1
        
        common = [c for c, count in conclusion_counts.items() if count > 1]
        report.common_conclusions = common
        
        if all_conclusions:
            report.agreement_score = len(common) / (len(set(all_conclusions)) + 0.1)
        
        # 2. Rank by confidence
        ranked = []
        for name, res in successful.items():
            ranked.append({
                "name": name,
                "type": res.reasoner_type.value,
                "confidence": res.confidence,
                "conclusions_count": len(res.conclusions),
                "execution_time_ms": res.execution_time_ms
            })
        
        ranked.sort(key=lambda x: (-x["confidence"], x["execution_time_ms"]))
        report.ranked_results = ranked
        
        if ranked:
            report.best_reasoner = ranked[0]["name"]
        
        # 3. Identify conflicts (different conclusions for yes/no)
        yes_no_answers = {}
        for name, res in successful.items():
            for c in res.conclusions:
                c_lower = c.lower()
                if c_lower.startswith("có") or "có -" in c_lower:
                    yes_no_answers[name] = "CÓ"
                elif c_lower.startswith("không") or "không -" in c_lower or "không thể chứng minh" in c_lower:
                    yes_no_answers[name] = "KHÔNG"
        
        if len(set(yes_no_answers.values())) > 1:
            report.conflicts.append({
                "type": "yes_no_disagreement",
                "details": yes_no_answers
            })
        
        # 4. Generate comparison text
        report.comparison_text = self._format_comparison(results, report)
        
        return report
    
    def select_best(self, results: Dict[str, ReasonerResult]) -> Optional[ReasonerResult]:
        """
        Select the best result based on multiple criteria.
        
        Criteria (in order):
        1. Success status
        2. Confidence score
        3. Number of conclusions
        4. Execution time (faster = better)
        """
        if not results:
            return None
        
        successful = [res for res in results.values() if res.success]
        
        if not successful:
            # Return first failed result
            return list(results.values())[0]
        
        # Sort by confidence (desc), conclusions (desc), time (asc)
        successful.sort(key=lambda x: (
            -x.confidence,
            -len(x.conclusions),
            x.execution_time_ms
        ))
        
        return successful[0]
    
    def _format_comparison(
        self, 
        results: Dict[str, ReasonerResult], 
        report: ComparisonReport
    ) -> str:
        """Generate human-readable comparison report."""
        lines = []
        lines.append("=" * 50)
        lines.append("BÁO CÁO SO SÁNH CÁC BỘ SUY DIỄN")
        lines.append("=" * 50)
        
        lines.append(f"\nTổng số reasoners: {report.total_reasoners}")
        lines.append(f"Thành công: {report.successful_reasoners}")
        lines.append(f"Điểm đồng thuận: {report.agreement_score:.2f}")
        
        if report.best_reasoner:
            lines.append(f"Reasoner tốt nhất: **{report.best_reasoner}**")
        
        lines.append("\n--- CHI TIẾT TỪNG REASONER ---")
        
        for name, res in results.items():
            lines.append(f"\n[{name}] ({res.reasoner_type.value})")
            lines.append(f"  Trạng thái: {'✓ Thành công' if res.success else '✗ Thất bại'}")
            lines.append(f"  Độ tin cậy: {res.confidence:.2f}")
            lines.append(f"  Thời gian: {res.execution_time_ms:.1f}ms")
            
            if res.conclusions:
                lines.append(f"  Kết luận ({len(res.conclusions)}):")
                # Hiển thị TẤT CẢ kết luận, KHÔNG giới hạn
                for c in res.conclusions:
                    lines.append(f"    • {c}")  # Full content, no truncation
            
            if res.proof_path:
                lines.append(f"  Proof path: {' -> '.join(res.proof_path)}")  # Full path
        
        if report.conflicts:
            lines.append("\n--- XUNG ĐỘT ---")
            for conflict in report.conflicts:
                lines.append(f"  ! {conflict['type']}: {conflict['details']}")
        
        if report.common_conclusions:
            lines.append("\n--- KẾT LUẬN CHUNG ---")
            # Hiển thị TẤT CẢ kết luận chung
            for c in report.common_conclusions:
                lines.append(f"  ✓ {c}")
        
        lines.append("\n" + "=" * 50)
        
        return "\n".join(lines)
    
    def get_consensus_answer(self, results: Dict[str, ReasonerResult]) -> str:
        """
        Generate a consensus answer combining all reasoner outputs.
        Returns raw formatted answer (non-LLM polished).
        """
        report = self.compare(results)
        best = self.select_best(results)
        
        if not best or not best.success:
            return "Không có đủ thông tin để trả lời."
        
        # Build consensus answer
        lines = []
        
        # Main answer from best reasoner
        if best.conclusions:
            lines.append(f"**Trả lời** (từ {best.reasoner_name}, độ tin cậy {best.confidence:.0%}):")
            for c in best.conclusions:
                lines.append(f"• {c}")
        
        # Add agreement info
        if report.agreement_score > 0.5:
            lines.append(f"\n_({report.successful_reasoners}/{report.total_reasoners} reasoners đồng thuận)_")
        
        # Add conflicts warning
        if report.conflicts:
            lines.append("\n⚠️ Lưu ý: Có sự khác biệt giữa các bộ suy diễn.")
        
        return "\n".join(lines)
    
    async def get_polished_answer(
        self, 
        results: Dict[str, ReasonerResult], 
        question: str,
        llm_service
    ) -> str:
        """
        Generate a polished consensus answer using LLM.
        LLM is used ONLY to make the text fluent, NOT to add new information.
        """
        report = self.compare(results)
        best = self.select_best(results)
        
        if not best or not best.success:
            return "Không có đủ thông tin để trả lời câu hỏi này."
        
        # Collect ALL conclusions from all reasoners - KHÔNG giới hạn
        all_data = []
        for name, res in results.items():
            if res.success and res.conclusions:
                for c in res.conclusions:
                    if c not in all_data:
                        all_data.append(c)
                
                # Also add evidence details - KHÔNG giới hạn
                for ev in res.evidence:
                    if isinstance(ev, dict):
                        ev_str = str(ev.get('value') or ev.get('content') or ev.get('text', ''))
                        if ev_str and ev_str not in all_data:
                            all_data.append(ev_str)
        
        # Build raw data string - KHÔNG giới hạn số lượng
        raw_data = "\n".join([f"- {d}" for d in all_data])
        
        # Use LLM to polish - BẮT BUỘC tiếng Việt, format bullet
        polish_prompt = f"""BẠN LÀ TRỢ LÝ VIẾT VĂN PHÁP LUẬT TIẾNG VIỆT.

CÂU HỎI: {question}

DỮ LIỆU THÔ:
{raw_data}

NHIỆM VỤ: Viết lại thành danh sách gạch đầu dòng tiếng Việt.

QUY TẮC BẮT BUỘC:
1. PHẢI viết 100% TIẾNG VIỆT - KHÔNG dùng tiếng Anh
2. Mỗi thông tin một dòng, bắt đầu bằng "•"
3. Cuối mỗi dòng PHẢI có căn cứ pháp lý (nếu có trong dữ liệu)
4. KHÔNG thêm thông tin mới, KHÔNG bịa đặt
5. Giữ nguyên TẤT CẢ nội dung, viết lại cho mạch lạc

VIẾT NGAY (TIẾNG VIỆT):"""
        
        try:
            polished = await llm_service.generate_response(polish_prompt, temperature=0.0)
            
            # Add source attribution
            result_lines = [polished.strip()]
            result_lines.append(f"\n\n_(Nguồn: {best.reasoner_name} | Độ tin cậy: {best.confidence:.0%} | {report.successful_reasoners}/{report.total_reasoners} reasoners)_")
            
            return "\n".join(result_lines)
            
        except Exception as e:
            # Fallback to raw answer
            return self.get_consensus_answer(results)

