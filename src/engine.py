import json
import os
from typing import List, Dict, Optional, Tuple
from .models import EngineeringParameter, InventivePrinciple, SolutionReport, IdealityFactor

class TRIZEngine:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.parameters: Dict[int, EngineeringParameter] = {}
        self.principles: Dict[int, InventivePrinciple] = {}
        self.matrix: Dict[str, List[int]] = {}
        self._load_data()

    def _load_data(self):
        # Load Parameters
        try:
            with open(os.path.join(self.data_dir, "parameters.json"), "r", encoding="utf-8") as f:
                params_data = json.load(f)
                for p in params_data:
                    self.parameters[p["id"]] = EngineeringParameter(**p)
        except Exception as e:
            print(f"Error loading parameters: {e}")

        # Load Principles
        try:
            with open(os.path.join(self.data_dir, "principles.json"), "r", encoding="utf-8") as f:
                princ_data = json.load(f)
                for p in princ_data:
                    self.principles[p["id"]] = InventivePrinciple(**p)
        except Exception as e:
            print(f"Error loading principles: {e}")

        # Load Matrix
        try:
            with open(os.path.join(self.data_dir, "matrix.json"), "r", encoding="utf-8") as f:
                self.matrix = json.load(f)
        except Exception as e:
            print(f"Error loading matrix: {e}")

    def normalize_input_to_parameter(self, user_text: str) -> Tuple[Optional[EngineeringParameter], List[str]]:
        """
        Returns (BestMatchParameter, LogMessages)
        """
        user_text = user_text.lower()
        best_match = None
        max_score = 0
        logs = []
        
        logs.append(f"Analyzing input: '{user_text}'")

        candidates = []

        for param in self.parameters.values():
            score = 0
            matched_kws = []
            for kw in param.keywords:
                # Simple substring match
                if kw.lower() in user_text:
                    score += 1
                    matched_kws.append(kw)
            
            if score > 0:
                candidates.append((param, score, matched_kws))
                if score > max_score:
                    max_score = score
                    best_match = param

        # Sort candidates by score
        candidates.sort(key=lambda x: x[1], reverse=True)
        
        if candidates:
            top_3 = candidates[:3]
            logs.append(f"Found {len(candidates)} potential candidates.")
            for p, s, kws in top_3:
                logs.append(f" - Candidate [{p.id}] '{p.name}': Score {s} (Keywords: {kws})")
        else:
            logs.append("No keywords matched.")

        if best_match:
            logs.append(f"Primary match selected: ID {best_match.id}")

        return best_match, logs

    def solve_contradiction(self, imp_id: int, wor_id: int) -> SolutionReport:
        logs = []
        logs.append(f"Initiating TRIZ Logic Block: Matrix Lookup")
        
        improving = self.parameters.get(imp_id)
        worsening = self.parameters.get(wor_id)

        if not improving or not worsening:
            raise ValueError("Invalid Parameter IDs")

        logs.append(f"Improving Parameter: [{imp_id}] {improving.name}")
        logs.append(f"Worsening Parameter: [{wor_id}] {worsening.name}")

        # Check for Physical Contradiction
        if imp_id == wor_id:
            logs.append("!! PHYSICAL CONTRADICTION DETECTED !! (A vs A)")
            logs.append("Switching logic to SEPARATION PRINCIPLES.")
            sep_principles = [
                InventivePrinciple(id=999, name="Separation in Time (時間分離)", description="Separate conflicting properties in time. (在時間上分離矛盾特性)", examples=["Traffic lights separte flow"]),
                InventivePrinciple(id=998, name="Separation in Space (空間分離)", description="Separate conflicting properties in space. (在空間上分離矛盾特性)", examples=["Bicycle path vs Car lane"])
            ]
            return SolutionReport(
                improving_parameter=improving,
                worsening_parameter=worsening,
                suggested_principles=sep_principles,
                strategy_note="PHYSICAL CONTRADICTION (物理矛盾)",
                execution_log=logs
            )

        # Lookup Matrix
        key = f"{imp_id},{wor_id}"
        logs.append(f"Querying Matrix Cell [{imp_id}, {wor_id}]...")
        principle_ids = self.matrix.get(key, [])

        note = ""
        suggested = []

        if not principle_ids:
            logs.append("Matrix Cell is EMPTY (No classic recommendation).")
            logs.append("Applying HEURISTIC FALLBACK (Top 4 general principles).")
            principle_ids = [35, 10, 1, 28] 
            note = "Heuristic Fallback (啟發式建議 - 矩陣無直接對應)"
        else:
            logs.append(f"Matrix Match Found! Principles: {principle_ids}")
            note = "Standard Matrix Solution (標準矩陣解)"

        for pid in principle_ids:
            p = self.principles.get(pid)
            if p:
                suggested.append(p)
            else:
                logs.append(f"Warning: Principle ID {pid} not found in database.")

        return SolutionReport(
            improving_parameter=improving,
            worsening_parameter=worsening,
            suggested_principles=suggested,
            strategy_note=note,
            execution_log=logs
        )

    def calculate_ideality(self, benefits: List[IdealityFactor], costs: List[IdealityFactor], harms: List[IdealityFactor]) -> float:
        num = sum(b.weight for b in benefits)
        den = sum(c.weight for c in costs) + sum(h.weight for h in harms)
        if den == 0:
            return 9999.0 # Infinity
        return round(num / den, 2)
