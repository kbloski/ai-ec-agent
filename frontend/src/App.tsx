import { Route, Routes } from 'react-router-dom'
import { AppShell } from '@/components/AppShell'
import OffersPage from '@/pages/OffersPage'
import OfferDetailPage from '@/pages/OfferDetailPage'
import KnowledgeDetailPage from '@/pages/KnowledgeDetailPage'
import TargetAudienceDetailPage from '@/pages/TargetAudienceDetailPage'
import AnalysisDetailPage from '@/pages/AnalysisDetailPage'
import ChecklistDetailPage from '@/pages/ChecklistDetailPage'
import BrandMarketingDetailPage from '@/pages/BrandMarketingDetailPage'
import MarketingStrategyDetailPage from '@/pages/MarketingStrategyDetailPage'
import OfferStrategyDetailPage from '@/pages/OfferStrategyDetailPage'
import MessageStrategyDetailPage from '@/pages/MessageStrategyDetailPage'
import AdStrategyDetailPage from '@/pages/AdStrategyDetailPage'
import CreativeStrategyDetailPage from '@/pages/CreativeStrategyDetailPage'
import AdExecutionDetailPage from '@/pages/AdExecutionDetailPage'
import UgcCreativeDetailPage from '@/pages/UgcCreativeDetailPage'
import PageStrategyDetailPage from '@/pages/PageStrategyDetailPage'
import PageBlueprintDetailPage from '@/pages/PageBlueprintDetailPage'
import PageContentPlanDetailPage from '@/pages/PageContentPlanDetailPage'
import PageCopyDetailPage from '@/pages/PageCopyDetailPage'

function App() {
  return (
    <Routes>
      <Route element={<AppShell />}>
        <Route path="/" element={<OffersPage />} />
        <Route path="/offers/:offerId" element={<OfferDetailPage />} />
        <Route path="/knowledges/:knowledgeId" element={<KnowledgeDetailPage />} />
        <Route path="/target-audiences/:id" element={<TargetAudienceDetailPage />} />
        <Route path="/knowledges/:knowledgeId/analysis/:analysisId" element={<AnalysisDetailPage />} />
        <Route
          path="/knowledges/:knowledgeId/analysis/:analysisId/checklists/:checklistId"
          element={<ChecklistDetailPage />}
        />
        <Route path="/brand-marketing/:id" element={<BrandMarketingDetailPage />} />
        <Route path="/marketing-strategy/:id" element={<MarketingStrategyDetailPage />} />
        <Route path="/offer-strategy/:id" element={<OfferStrategyDetailPage />} />
        <Route path="/message-strategy/:id" element={<MessageStrategyDetailPage />} />
        <Route path="/ad-strategy/:id" element={<AdStrategyDetailPage />} />
        <Route path="/creative-strategy/:id" element={<CreativeStrategyDetailPage />} />
        <Route path="/ad-execution/:id" element={<AdExecutionDetailPage />} />
        <Route path="/ugc-creatives/:id" element={<UgcCreativeDetailPage />} />
        <Route path="/page-strategy/:id" element={<PageStrategyDetailPage />} />
        <Route path="/page-blueprint/:id" element={<PageBlueprintDetailPage />} />
        <Route path="/page-content-plan/:id" element={<PageContentPlanDetailPage />} />
        <Route path="/page-copy/:id" element={<PageCopyDetailPage />} />
      </Route>
    </Routes>
  )
}

export default App
