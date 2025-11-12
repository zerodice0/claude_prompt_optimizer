"""
Template Manager for Claude Prompt Optimizer
도메인별 프롬프트 템플릿 관리 시스템
"""

import json
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


@dataclass
class Template:
    """프롬프트 템플릿"""
    id: str
    name: str
    domain: str
    intent: str
    template: str
    variables: List[str]
    description: str
    example_usage: str
    complexity: str  # low, medium, high


class TemplateManager:
    """템플릿 관리 시스템"""

    def __init__(self, patterns_dir: str = None):
        if patterns_dir is None:
            # 기본 패턴 디렉토리 경로
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.patterns_dir = os.path.join(current_dir, "..", "references", "patterns")
        else:
            self.patterns_dir = patterns_dir

        self.templates = {}
        self.domain_patterns = {}
        self.load_patterns()

    def load_patterns(self):
        """도메인별 패턴 파일 로드"""
        domains = ["development", "marketing", "content", "business"]

        for domain in domains:
            pattern_file = os.path.join(self.patterns_dir, f"{domain}.json")
            if os.path.exists(pattern_file):
                try:
                    with open(pattern_file, 'r', encoding='utf-8') as f:
                        self.domain_patterns[domain] = json.load(f)
                except Exception as e:
                    print(f"Warning: Failed to load {domain} patterns: {e}")
                    self.domain_patterns[domain] = {}
            else:
                self.domain_patterns[domain] = {}

        # 기본 템플릿 생성
        self.generate_default_templates()

    def generate_default_templates(self):
        """기본 템플릿 생성"""
        default_templates = [
            # Development Templates
            Template(
                id="code_review",
                name="코드 리뷰 요청",
                domain="development",
                intent="analyze",
                template="시니어 개발자로서 다음 코드의 품질, 성능, 보안 측면에서 리뷰를 제공해주세요. {focus}에 특히 집중해주시고, 구체적인 개선 사항과 코드 예시를 포함해주세요. {additional_requirements}",
                variables=["focus", "additional_requirements"],
                description="코드의 품질과 개선점을 종합적으로 분석해달라는 요청",
                example_usage="focus=성능 최적화, additional_requirements=시간 복잡도 분석 포함",
                complexity="medium"
            ),
            Template(
                id="debug_help",
                name="디버깅 도움 요청",
                domain="development",
                intent="fix",
                template="디버깅 전문가로서 다음 에러를 분석하고 해결책을 제안해주세요. 오류 메시지: {error_message}. 발생 환경: {context}. 가능한 원인과 해결 단계를 구체적으로 설명해주세요. {additional_context}",
                variables=["error_message", "context", "additional_context"],
                description="프로그래밍 에러의 원인 분석과 해결책 요청",
                example_usage="error_message=TypeError in line 42, context=React component rendering",
                complexity="high"
            ),
            Template(
                id="architecture_design",
                name="아키텍처 설계",
                domain="development",
                intent="create",
                template="소프트웨어 아키텍트로서 {project_type} 프로젝트의 아키텍처를 설계해주세요. 주요 요구사항: {requirements}. 확장성, 유지보수성, 성능을 고려하여 구성 요소와 상호작용을 설명해주세요. {tech_stack} 기반으로 설계해주세요.",
                variables=["project_type", "requirements", "tech_stack"],
                description="소프트웨어 시스템의 아키텍처 설계 요청",
                example_usage="project_type=전자상거래, requirements=실시간 재고 관리, tech_stack=Microservices",
                complexity="high"
            ),

            # Marketing Templates
            Template(
                id="campaign_strategy",
                name="마케팅 캠페인 전략",
                domain="marketing",
                intent="plan",
                template="마케팅 전략가로서 {product}의 마케팅 캠페인을 기획해주세요. 타겟: {target_audience}. 목표: {campaign_goals}. 채널: {channels}. 구체적인 실행 계획과 예상 효과를 포함해주세요. {additional_requirements}",
                variables=["product", "target_audience", "campaign_goals", "channels", "additional_requirements"],
                description="제품/서비스의 마케팅 캠페인 전략 수립",
                example_usage="product=AI 헬스케어 앱, target_audience=2030대 건강 관심층, campaign_goals=가입자 1만명",
                complexity="high"
            ),
            Template(
                id="copywriting",
                name="카피라이팅",
                domain="marketing",
                intent="create",
                template="전문 카피라이터로서 {product}의 마케팅 문구를 작성해주세요. 대상: {target}. 목적: {purpose}. 톤앤매너: {tone}. 핵심 장점을 강조하고 행동 촉구를 포함해주세요. {format}으로 작성해주세요.",
                variables=["product", "target", "purpose", "tone", "format"],
                description="마케팅 광고 문구 작성",
                example_usage="product=유기농 주스, target=건강한 라이프스타일 추구자, purpose=구매 유도",
                complexity="medium"
            ),

            # Content Templates
            Template(
                id="blog_post",
                name="블로그 글 작성",
                domain="content",
                intent="create",
                template="전문 작가로서 '{title}' 주제의 블로그 글을 작성해주세요. 대상 독자: {audience}. 길이: {length}. 키워드: {keywords}. 톤앤매너: {tone}. SEO를 고려하고 실용적인 정보를 제공해주세요. 구조: {structure}.",
                variables=["title", "audience", "length", "keywords", "tone", "structure"],
                description="SEO 최적화된 블로그 글 작성",
                example_usage="title=AI 업무 자동화, audience=IT 관리자, length=1500자",
                complexity="medium"
            ),
            Template(
                id="social_media",
                name="소셜 미디어 콘텐츠",
                domain="content",
                intent="create",
                template="콘텐츠 크리에이터로서 {platform} 플랫폼용 게시물을 작성해주세요. 주제: {topic}. 대상: {audience}. 목적: {goal}. 해시태그: {hashtags}. 이미지/영상과 함께 사용할 수 있도록 작성해주세요. {engagement_elements} 포함해주세요.",
                variables=["platform", "topic", "audience", "goal", "hashtags", "engagement_elements"],
                description="소셜 미디어 플랫폼용 콘텐츠 제작",
                example_usage="platform=Instagram, topic=자기계발, audience=2030대 직장인",
                complexity="low"
            ),

            # Business Templates
            Template(
                id="business_proposal",
                name="비즈니스 제안서",
                domain="business",
                intent="create",
                template="비즈니스 컨설턴트로서 {project} 제안서를 작성해주세요. 고객사: {client}. 문제점: {problem}. 해결책: {solution}. 예상 효과: {benefits}. 예산: {budget}. 실행 계획과 ROI를 포함해주세요. {format}으로 정리해주세요.",
                variables=["project", "client", "problem", "solution", "benefits", "budget", "format"],
                description="프로젝트나 솔루션 제안서 작성",
                example_usage="project=업무 자동화 시스템, client=중소 제조업체, problem=반복 작업 비효율",
                complexity="high"
            ),
            Template(
                id="email_template",
                name="비즈니스 이메일",
                domain="business",
                intent="create",
                template="전문적인 비즈니스 이메일을 작성해주세요. 수신자: {recipient}. 목적: {purpose}. 주요 내용: {content}. 마감일: {deadline}. 형식: {email_type}. 명확하고 간결하게 작성해주세요. {additional_requirements}.",
                variables=["recipient", "purpose", "content", "deadline", "email_type", "additional_requirements"],
                description="다양한 목적의 비즈니스 이메일 작성",
                example_usage="recipient=팀원, purpose=프로젝트 진행 상황 공유, email_type=업데이트 보고",
                complexity="low"
            ),
        ]

        # 템플릿 등록
        for template in default_templates:
            self.templates[template.id] = template

    def get_template(self, template_id: str) -> Optional[Template]:
        """템플릿 ID로 템플릿 조회"""
        return self.templates.get(template_id)

    def get_templates_by_domain(self, domain: str) -> List[Template]:
        """도메인별 템플릿 조회"""
        return [template for template in self.templates.values() if template.domain == domain]

    def get_templates_by_intent(self, intent: str) -> List[Template]:
        """의도별 템플릿 조회"""
        return [template for template in self.templates.values() if template.intent == intent]

    def find_best_template(self, domain: str, intent: str, complexity: str = "medium") -> Optional[Template]:
        """최적의 템플릿 찾기"""
        candidates = []

        for template in self.templates.values():
            if template.domain == domain and template.intent == intent:
                # 복잡도 일치 시 가장 높은 우선순위
                if template.complexity == complexity:
                    return template
                candidates.append(template)

        # 정확히 일치하는 복잡도가 없으면 가장 가까운 복잡도로 선택
        if candidates:
            complexity_order = {"low": 0, "medium": 1, "high": 2}
            target_level = complexity_order.get(complexity, 1)

            # 복잡도 차이가 가장 적은 템플릿 선택
            best_candidate = min(candidates,
                                key=lambda t: abs(complexity_order.get(t.complexity, 1) - target_level))
            return best_candidate

        return None

    def fill_template(self, template: Template, variables: Dict[str, str]) -> str:
        """템플릿에 변수 값 채우기"""
        filled = template.template

        for var_name, var_value in variables.items():
            placeholder = "{" + var_name + "}"
            filled = filled.replace(placeholder, var_value)

        # 채워지지 않은 변수가 있다면 안내 메시지 추가
        remaining_vars = []
        for var in template.variables:
            if "{" + var + "}" in filled:
                remaining_vars.append(var)

        if remaining_vars:
            filled += f"\n\n필요한 정보: {', '.join(remaining_vars)}"

        return filled

    def suggest_variables(self, template_id: str, user_input: str) -> Dict[str, str]:
        """사용자 입력 기반으로 변수 값 추천"""
        template = self.get_template(template_id)
        if not template:
            return {}

        suggestions = {}
        user_input_lower = user_input.lower()

        # 템플릿별 변수 추천 로직
        if template.domain == "development":
            if "error" in user_input_lower or "에러" in user_input_lower:
                suggestions["error_message"] = user_input
            if "bug" in user_input_lower or "버그" in user_input_lower:
                suggestions["context"] = "개발 환경"

        elif template.domain == "marketing":
            if "product" in user_input_lower or "제품" in user_input_lower:
                suggestions["product"] = user_input
            if "target" in user_input_lower or "타겟" in user_input_lower:
                suggestions["target_audience"] = "2030대"

        elif template.domain == "content":
            if "blog" in user_input_lower or "블로그" in user_input_lower:
                suggestions["format"] = "블로그 글"
            if "social" in user_input_lower or "소셜" in user_input_lower:
                suggestions["platform"] = "Instagram"

        elif template.domain == "business":
            if "email" in user_input_lower or "이메일" in user_input_lower:
                suggestions["email_type"] = "업무 이메일"
            if "proposal" in user_input_lower or "제안" in user_input_lower:
                suggestions["format"] = "제안서 형식"

        return suggestions

    def get_template_recommendations(self, domain: str, user_input: str, complexity: str = "medium") -> List[Template]:
        """사용자 입력 기반 템플릿 추천"""
        user_input_lower = user_input.lower()
        recommendations = []

        # 의도 감지
        intent_keywords = {
            "create": ["만들", "생성", "작성", "개발", "제작", "기획"],
            "analyze": ["분석", "리뷰", "평가", "검토", "조사"],
            "fix": ["수정", "해결", "버그", "오류", "문제"],
            "plan": ["계획", "전략", "방안", "로드맵"]
        }

        detected_intent = "general"
        for intent, keywords in intent_keywords.items():
            if any(keyword in user_input_lower for keyword in keywords):
                detected_intent = intent
                break

        # 도메인 및 의도에 맞는 템플릿 찾기
        if detected_intent != "general":
            best_template = self.find_best_template(domain, detected_intent, complexity)
            if best_template:
                recommendations.append(best_template)

        # 추가 관련 템플릿 추천
        domain_templates = self.get_templates_by_domain(domain)
        for template in domain_templates:
            if template not in recommendations and len(recommendations) < 3:
                # 사용자 입력에 템플릿 키워드가 포함되어 있는지 확인
                template_keywords = template.name.lower().split()
                if any(keyword in user_input_lower for keyword in template_keywords):
                    recommendations.append(template)

        return recommendations

    def create_custom_template(self, template_data: Dict[str, Any]) -> Template:
        """사용자 정의 템플릿 생성"""
        return Template(
            id=template_data["id"],
            name=template_data["name"],
            domain=template_data["domain"],
            intent=template_data["intent"],
            template=template_data["template"],
            variables=template_data.get("variables", []),
            description=template_data.get("description", ""),
            example_usage=template_data.get("example_usage", ""),
            complexity=template_data.get("complexity", "medium")
        )

    def save_custom_template(self, template: Template, filename: str = None):
        """사용자 정의 템플릿 저장"""
        if filename is None:
            filename = os.path.join(self.patterns_dir, f"custom_{template.id}.json")

        template_data = {
            "id": template.id,
            "name": template.name,
            "domain": template.domain,
            "intent": template.intent,
            "template": template.template,
            "variables": template.variables,
            "description": template.description,
            "example_usage": template.example_usage,
            "complexity": template.complexity
        }

        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(template_data, f, ensure_ascii=False, indent=2)

    def get_template_summary(self, template: Template) -> str:
        """템플릿 요약 정보"""
        summary = f"""📋 {template.name} (ID: {template.id})
• 도메인: {template.domain}
• 의도: {template.intent}
• 복잡도: {template.complexity}
• 설명: {template.description}
• 변수: {', '.join(template.variables) if template.variables else '없음'}
• 사용 예시: {template.example_usage}

템플릿:
{template.template}"""
        return summary


# 사용 예시
if __name__ == "__main__":
    manager = TemplateManager()

    # 템플릿 조회 예시
    template = manager.get_template("code_review")
    if template:
        print(manager.get_template_summary(template))

        # 변수 채우기 예시
        variables = {
            "focus": "성능 최적화",
            "additional_requirements": "시간 복잡도 분석 포함"
        }
        filled = manager.fill_template(template, variables)
        print(f"\n채워진 템플릿:\n{filled}")

    # 템플릿 추천 예시
    recommendations = manager.get_template_recommendations("development", "코드 리뷰 부탁드립니다")
    print(f"\n추천 템플릿: {[t.name for t in recommendations]}")