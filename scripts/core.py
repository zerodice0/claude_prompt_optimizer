"""
Claude Prompt Optimizer Core Engine
메인 최적화 엔진 - 통합 관리 및 실행
"""

import json
import os
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from .analyzer import PromptAnalyzer, AnalysisResult, Domain, OptimizationLevel
from .optimizer import PromptOptimizer, OptimizationResult
from .templates import TemplateManager, Template


class ExecutionMode(Enum):
    OPTIMIZE = "optimize"
    ANALYZE = "analyze"
    TEMPLATE = "template"
    AUTO = "auto"


@dataclass
class OptimizationRequest:
    """최적화 요청"""
    prompt: str
    domain: Domain = Domain.AUTO
    optimization_level: OptimizationLevel = OptimizationLevel.BALANCED
    execution_mode: ExecutionMode = ExecutionMode.AUTO
    show_analysis: bool = True
    template_id: Optional[str] = None
    template_variables: Optional[Dict[str, str]] = None


@dataclass
class OptimizationResponse:
    """최적화 응답"""
    success: bool
    original_prompt: str
    optimized_prompt: Optional[str] = None
    analysis: Optional[AnalysisResult] = None
    optimization: Optional[OptimizationResult] = None
    template: Optional[Template] = None
    message: str = ""
    execution_time: float = 0.0
    recommendations: List[str] = None


class ClaudePromptOptimizer:
    """Claude 프롬프트 최적기 메인 엔진"""

    def __init__(self, patterns_dir: str = None):
        self.analyzer = PromptAnalyzer()
        self.optimizer = PromptOptimizer()
        self.template_manager = TemplateManager(patterns_dir)
        self.execution_history = []

    def process_request(self, request: OptimizationRequest) -> OptimizationResponse:
        """최적화 요청 처리"""
        import time
        start_time = time.time()

        try:
            # 실행 모드 결정
            if request.execution_mode == ExecutionMode.AUTO:
                execution_mode = self._determine_execution_mode(request)
            else:
                execution_mode = request.execution_mode

            # 분석 수행
            analysis = self.analyzer.analyze(
                request.prompt,
                request.domain,
                request.optimization_level
            )

            response = OptimizationResponse(
                success=True,
                original_prompt=request.prompt,
                analysis=analysis
            )

            # 실행 모드별 처리
            if execution_mode == ExecutionMode.TEMPLATE:
                # 템플릿 모드
                template_result = self._process_template_mode(request, analysis)
                response.template = template_result["template"]
                response.optimized_prompt = template_result["filled_template"]
                response.recommendations = template_result["recommendations"]

            elif execution_mode == ExecutionMode.ANALYZE:
                # 분석 모드
                response.message = self.analyzer.get_analysis_summary(analysis)

            else:
                # 최적화 모드 (기본)
                optimization = self.optimizer.optimize(analysis)
                response.optimization = optimization
                response.optimized_prompt = optimization.optimized_prompt
                response.message = self.optimizer.get_optimization_summary(optimization)

                # 템플릿 추천
                template_recommendations = self._get_template_recommendations(request, analysis)
                if template_recommendations:
                    response.recommendations = [f"템플릿 추천: {t.name}" for t in template_recommendations[:3]]

            response.execution_time = time.time() - start_time

            # 실행 기록 저장
            self.execution_history.append({
                "timestamp": time.time(),
                "request": request,
                "response": response
            })

            return response

        except Exception as e:
            return OptimizationResponse(
                success=False,
                original_prompt=request.prompt,
                message=f"오류가 발생했습니다: {str(e)}",
                execution_time=time.time() - start_time
            )

    def _determine_execution_mode(self, request: OptimizationRequest) -> ExecutionMode:
        """실행 모드 자동 결정"""
        # 템플릿 ID가 지정된 경우
        if request.template_id:
            return ExecutionMode.TEMPLATE

        # 프롬프트가 너무 짧은 경우 템플릿 추천
        if len(request.prompt.split()) < 5:
            return ExecutionMode.TEMPLATE

        # 분석만 요청하는 경우
        if request.prompt.startswith("/") and "analyze" in request.prompt.lower():
            return ExecutionMode.ANALYZE

        # 기본 최적화 모드
        return ExecutionMode.OPTIMIZE

    def _process_template_mode(self, request: OptimizationRequest, analysis: AnalysisResult) -> Dict[str, Any]:
        """템플릿 모드 처리"""
        result = {
            "template": None,
            "filled_template": None,
            "recommendations": []
        }

        # 템플릿 선택
        if request.template_id:
            template = self.template_manager.get_template(request.template_id)
        else:
            # 최적의 템플릿 추천 (의미 기반 매칭 우선)
            template = self.template_manager.find_best_template_semantic(
                request.prompt,
                analysis.domain.value,
                analysis.detected_intent
            )

        if template:
            result["template"] = template

            # 변수 값 준비
            variables = request.template_variables or {}
            if not variables:
                # 사용자 입력 기반 변수 추천
                suggested_vars = self.template_manager.suggest_variables(template.id, request.prompt)
                variables = suggested_vars

            # 템플릿 채우기
            filled_template = self.template_manager.fill_template(template, variables)

            if filled_template is None:
                # 변수가 완전히 채워지지 않은 경우 부분 채우기
                partial_filled, missing_vars = self.template_manager.fill_template_partial(template, variables)
                result["filled_template"] = partial_filled
                result["missing_variables"] = missing_vars
                result["recommendations"].append(f"누락된 변수: {', '.join(missing_vars)}")
            else:
                result["filled_template"] = filled_template

        else:
            # 템플릿을 찾지 못한 경우 추천 목록 제공
            recommendations = self.template_manager.get_template_recommendations(
                analysis.domain.value,
                request.prompt,
                analysis.complexity_level
            )
            result["recommendations"] = [f"추천 템플릿: {t.name} (ID: {t.id})" for t in recommendations]

        return result

    def _get_template_recommendations(self, request: OptimizationRequest, analysis: AnalysisResult) -> List[Template]:
        """템플릿 추천"""
        return self.template_manager.get_template_recommendations(
            analysis.domain.value,
            request.prompt,
            analysis.complexity_level
        )

    def optimize_prompt(self, prompt: str, domain: str = "auto",
                        optimization_level: str = "balanced",
                        show_analysis: bool = True) -> Dict[str, Any]:
        """간편 최적화 함수"""
        try:
            # 도메인 변환
            domain_enum = Domain(domain) if domain != "auto" else Domain.AUTO

            # 최적화 레벨 변환
            level_enum = OptimizationLevel(optimization_level)

            # 요청 생성
            request = OptimizationRequest(
                prompt=prompt,
                domain=domain_enum,
                optimization_level=level_enum,
                show_analysis=show_analysis
            )

            # 처리
            response = self.process_request(request)

            if response.success:
                result = {
                    "success": True,
                    "original_prompt": response.original_prompt,
                    "optimized_prompt": response.optimized_prompt,
                    "analysis": None,
                    "optimization": None,
                    "message": response.message,
                    "execution_time": response.execution_time,
                    "recommendations": response.recommendations or []
                }

                # 분석 결과 포함
                if response.analysis and show_analysis:
                    result["analysis"] = {
                        "domain": response.analysis.domain.value,
                        "intent": response.analysis.detected_intent,
                        "complexity": response.analysis.complexity_level,
                        "scores": response.analysis.scores,
                        "total_score": response.analysis.total_score,
                        "token_count": response.analysis.token_count
                    }

                # 최적화 결과 포함
                if response.optimization:
                    result["optimization"] = {
                        "token_reduction": response.optimization.token_reduction,
                        "token_reduction_percent": response.optimization.token_reduction_percent,
                        "optimization_score": response.optimization.optimization_score,
                        "applied_techniques": response.optimization.applied_techniques,
                        "improvement_areas": response.optimization.improvement_areas
                    }

                return result

            else:
                return {
                    "success": False,
                    "message": response.message,
                    "execution_time": response.execution_time
                }

        except Exception as e:
            return {
                "success": False,
                "message": f"처리 중 오류 발생: {str(e)}",
                "execution_time": 0.0
            }

    def analyze_prompt(self, prompt: str, domain: str = "auto") -> Dict[str, Any]:
        """프롬프트 분석 전용 함수"""
        try:
            domain_enum = Domain(domain) if domain != "auto" else Domain.AUTO
            analysis = self.analyzer.analyze(prompt, domain_enum)

            return {
                "success": True,
                "original_prompt": analysis.original_prompt,
                "domain": analysis.domain.value,
                "intent": analysis.detected_intent,
                "complexity": analysis.complexity_level,
                "scores": analysis.scores,
                "total_score": analysis.total_score,
                "token_count": analysis.token_count,
                "issues": analysis.issues,
                "suggestions": analysis.suggestions,
                "summary": self.analyzer.get_analysis_summary(analysis)
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"분석 중 오류 발생: {str(e)}"
            }

    def get_template_list(self, domain: str = None, intent: str = None) -> List[Dict[str, Any]]:
        """템플릿 목록 조회"""
        templates = []

        if domain:
            templates = self.template_manager.get_templates_by_domain(domain)
        elif intent:
            templates = self.template_manager.get_templates_by_intent(intent)
        else:
            templates = list(self.template_manager.templates.values())

        return [
            {
                "id": t.id,
                "name": t.name,
                "domain": t.domain,
                "intent": t.intent,
                "description": t.description,
                "complexity": t.complexity,
                "variables": t.variables,
                "example_usage": t.example_usage
            }
            for t in templates
        ]

    def use_template(self, template_id: str, variables: Dict[str, str]) -> Dict[str, Any]:
        """템플릿 사용"""
        try:
            template = self.template_manager.get_template(template_id)
            if not template:
                return {
                    "success": False,
                    "message": f"템플릿을 찾을 수 없습니다: {template_id}"
                }

            filled_template = self.template_manager.fill_template(template, variables)

            return {
                "success": True,
                "template_id": template_id,
                "template_name": template.name,
                "filled_template": filled_template,
                "template_summary": self.template_manager.get_template_summary(template)
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"템플릿 처리 중 오류 발생: {str(e)}"
            }

    def get_statistics(self) -> Dict[str, Any]:
        """실행 통계"""
        if not self.execution_history:
            return {
                "total_executions": 0,
                "average_execution_time": 0.0,
                "success_rate": 0.0
            }

        total_executions = len(self.execution_history)
        successful_executions = sum(1 for h in self.execution_history if h["response"].success)
        total_time = sum(h["response"].execution_time for h in self.execution_history)

        # 도메인별 통계
        domain_stats = {}
        for history in self.execution_history:
            domain = history["response"].analysis.domain.value if history["response"].analysis else "unknown"
            domain_stats[domain] = domain_stats.get(domain, 0) + 1

        return {
            "total_executions": total_executions,
            "successful_executions": successful_executions,
            "success_rate": (successful_executions / total_executions * 100) if total_executions > 0 else 0,
            "average_execution_time": (total_time / total_executions) if total_executions > 0 else 0,
            "domain_distribution": domain_stats,
            "last_execution": self.execution_history[-1]["timestamp"] if self.execution_history else None
        }


# 전역 인스턴스 (싱글톤)
_optimizer_instance = None

def get_optimizer() -> ClaudePromptOptimizer:
    """전역 옵티마이저 인스턴스获取"""
    global _optimizer_instance
    if _optimizer_instance is None:
        _optimizer_instance = ClaudePromptOptimizer()
    return _optimizer_instance


# 간편 사용 함수
def optimize_prompt(prompt: str, domain: str = "auto", optimization_level: str = "balanced") -> Dict[str, Any]:
    """프롬프트 최적화 간편 함수"""
    return get_optimizer().optimize_prompt(prompt, domain, optimization_level)


def analyze_prompt(prompt: str, domain: str = "auto") -> Dict[str, Any]:
    """프롬프트 분석 간편 함수"""
    return get_optimizer().analyze_prompt(prompt, domain)


def list_templates(domain: str = None, intent: str = None) -> List[Dict[str, Any]]:
    """템플릿 목록 간편 함수"""
    return get_optimizer().get_template_list(domain, intent)


def use_template(template_id: str, variables: Dict[str, str]) -> Dict[str, Any]:
    """템플릿 사용 간편 함수"""
    return get_optimizer().use_template(template_id, variables)


# 사용 예시
if __name__ == "__main__":
    optimizer = get_optimizer()

    # 기본 최적화 예시
    result = optimizer.optimize_prompt("코드 리뷰를 부탁드립니다")
    print("=== 최적화 결과 ===")
    print(result["message"])

    # 분석 예시
    analysis = optimizer.analyze_prompt("블로그 글을 써줘")
    print("\n=== 분석 결과 ===")
    print(analysis["summary"])

    # 템플릿 목록 예시
    templates = optimizer.get_template_list(domain="development")
    print(f"\n=== 개발 도메인 템플릿 ({len(templates)}개) ===")
    for template in templates[:3]:  # 상위 3개만 표시
        print(f"• {template['name']} (ID: {template['id']})")

    # 통계 예시
    stats = optimizer.get_statistics()
    print(f"\n=== 실행 통계 ===")
    print(f"총 실행 횟수: {stats['total_executions']}")
    print(f"성공률: {stats['success_rate']:.1f}%")
    print(f"평균 실행 시간: {stats['average_execution_time']:.3f}초")