// server.js (Express)
const express = require('express');
const fetch = require('node-fetch'); // or global fetch in Node 18+
const app = express();

const PORT = process.env.PORT || 8002;

// Example using ip-api.com (no key needed). Replace with your provider if you have an API key.
app.get('/check-ip', async (req, res) => {
  const ip = (req.query.ip || '').trim();
  if (!ip) return res.status(400).json({ message: 'ip is required' });

  try {
    const resp = await fetch(`http://ip-api.com/json/${encodeURIComponent(ip)}?fields=status,message,query,country,isp`);
    const json = await resp.json();

    if (json.status !== 'success') {
      return res.status(400).json({ message: json.message || 'lookup failed', query: ip });
    }

    // Map to the shape expected by api-service/frontend
    res.json({
      query: json.query,
      reputation: 'Good',        // or compute if you have threat intel
      country: json.country,
      provider: json.isp,
      threats: []
    });
  } catch (e) {
    res.status(502).json({ message: 'upstream error', error: String(e), query: ip });
  }
});

app.listen(PORT, () => {
  console.log(`Analysis service listening on http://0.0.0.0:${PORT}`);
});
