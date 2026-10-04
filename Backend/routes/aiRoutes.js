const express = require('express');
const { recommend, skillGap, analytics } = require('../controllers/aiController');
const { protect } = require('../middleware/authMiddleware');

const router = express.Router();

router.use(protect);

router.get('/recommend', recommend);
router.get('/skill-gap', skillGap);
router.get('/analytics', analytics);

module.exports = router;
