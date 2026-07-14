from enum import Enum


class TableName(str, Enum):
    OFFERS = "offers"
    OFFER_ITEMS = "offer_items"
    OFFER_KNOWLEDGE = "knowledge"
    KNOWLEDGE_INSIGHTS = "knowledge_insights"
    OFFER_INSIGHTS = "offer_insights"
    TARGET_AUDIENCES = "target_audiences"
    ANALYSIS = "analysis"
    KNOWLEDGE_ANALYSIS = "knowledge_analysis"
    ANALYSIS_QUESTIONS= "analysis_questions"
    CHECKLIST = "checklist"
    CHECKLIST_ITEM = "checklist_item"
    ANALYSIS_CHECKLIST = "analysis_checklist"