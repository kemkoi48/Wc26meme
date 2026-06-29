exports.handler = async (event) => {
  try {
    // Free open-source WC 2026 API — no key required
    // Returns all matches with live scores, status, homeScore, awayScore
    const res = await fetch("https://worldcup26.ir/get/games");
    const data = await res.json();
    return {
      statusCode: 200,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    };
  } catch (e) {
    return {
      statusCode: 500,
      headers: { "Access-Control-Allow-Origin": "*" },
      body: JSON.stringify({ error: e.message }),
    };
  }
};
