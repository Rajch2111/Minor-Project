const aiService = require('../services/aiService');

// GET /api/ai/recommend?skills=...
exports.recommend = async (req, res, next) => {
  try {
    const { skills, topN } = req.query;
    if (!skills) {
      return res.status(400).json({ success: false, message: 'skills query param required' });
    }
    const data = await aiService.getRecommendations(skills, topN || 5);
    res.json({ success: true, data });
  } catch (err) {
    next(err);
  }
};

// GET /api/ai/skill-gap?target_role=...&skills=...
exports.skillGap = async (req, res, next) => {
  try {
    const { target_role, skills } = req.query;
    if (!target_role || !skills) {
      return res.status(400).json({ success: false, message: 'target_role and skills required' });
    }
    const data = await aiService.getSkillGap(target_role, skills);
    res.json({ success: true, data });
  } catch (err) {
    next(err);
  }
};

// GET /api/ai/analytics
exports.analytics = async (req, res, next) => {
  try {
    const data = await aiService.getAnalytics();
    res.json({ success: true, data });
  } catch (err) {
    next(err);
  }
};
