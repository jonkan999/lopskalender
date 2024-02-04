exports.handler = async (event, context) => {
  const MAPBOX_BASIC_STYLE_API_KEY = process.env.MAPBOX_BASIC_STYLE_API_KEY;
  return {
    statusCode: 200,
    body: JSON.stringify({ MAPBOX_BASIC_STYLE_API_KEY }),
  };
};
