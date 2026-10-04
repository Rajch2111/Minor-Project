/**
 * AI Service Client — forwards requests to the Python FastAPI AI-Service
 */
const AI_SERVICE_URL = process.env.AI_SERVICE_URL || 'http://localhost:8000';

const getRecommendations = async (skills, topN = 5) => {
  const res = await fetch(
    `${AI_SERVICE_URL}/recommend?skills=${encodeURIComponent(skills)}&top_n=${topN}`
  );
  if (!res.ok) throw new Error('AI service recommendation failed');
  return res.json();
};

const getSkillGap = async (targetRole, skills) => {
  const res = await fetch(
    `${AI_SERVICE_URL}/skill-gap?target_role=${encodeURIComponent(targetRole)}&skills=${encodeURIComponent(skills)}`
  );
  if (!res.ok) throw new Error('AI service skill-gap failed');
  return res.json();
};

const getAnalytics = async () => {
  const res = await fetch(`${AI_SERVICE_URL}/analytics`);
  if (!res.ok) throw new Error('AI service analytics failed');
  return res.json();
};

module.exports = { getRecommendations, getSkillGap, getAnalytics, AI_SERVICE_URL };
