/**
 * KidWatch Apps Script API
 *
 * Serves YouTube watch history data from the KidWatch Data Google Sheet as JSON.
 * Deploy as a Web App (Anyone can access) to get a public URL.
 *
 * Sheet ID: 1eJw4-GHMNTMK7ZKTOjYxdc_fvTac8PTjiLlVPsqoKgA
 *
 * Tab structure:
 *   Videos       — videoId, title, channel, channelId, watchedAt, duration, durationSeconds,
 *                  safetyScore, safetyRating, safetyBadge, flags, categories, url
 *   DailySummary — date, totalVideos, totalHours, flaggedCount, safetyScore, topChannels
 *   Channels     — channelId, channelName, videoCount, avgSafetyScore, flagCount, lastSeen
 */

const SHEET_ID = '1eJw4-GHMNTMK7ZKTOjYxdc_fvTac8PTjiLlVPsqoKgA';

function doGet(e) {
  try {
    const data = buildResponse();
    return ContentService
      .createTextOutput(JSON.stringify(data))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    const errResponse = { error: err.toString(), timestamp: new Date().toISOString() };
    return ContentService
      .createTextOutput(JSON.stringify(errResponse))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function buildResponse() {
  const ss = SpreadsheetApp.openById(SHEET_ID);

  return {
    videos: getVideos(ss),
    dailySummary: getDailySummary(ss),
    channels: getChannels(ss),
    generated: new Date().toISOString()
  };
}

/**
 * Read Videos tab — returns array matching history.json format
 */
function getVideos(ss) {
  const sheet = ss.getSheetByName('Videos');
  if (!sheet) return [];

  const data = sheet.getDataRange().getValues();
  if (data.length < 2) return [];

  const headers = data[0];
  const rows = data.slice(1).filter(r => r.some(c => c !== ''));

  return rows.map(row => {
    const obj = {};
    headers.forEach((h, i) => {
      if (!h) return;
      let val = row[i];
      // Parse JSON-encoded arrays (flags, categories)
      if (typeof val === 'string' && (val.startsWith('[') || val.startsWith('{'))) {
        try { val = JSON.parse(val); } catch (e) { /* keep as string */ }
      }
      // Format dates
      if (val instanceof Date) val = val.toISOString();
      obj[h] = val === '' ? null : val;
    });
    return obj;
  });
}

/**
 * Read DailySummary tab
 */
function getDailySummary(ss) {
  const sheet = ss.getSheetByName('DailySummary');
  if (!sheet) return [];

  const data = sheet.getDataRange().getValues();
  if (data.length < 2) return [];

  const headers = data[0];
  const rows = data.slice(1).filter(r => r.some(c => c !== ''));

  return rows.map(row => {
    const obj = {};
    headers.forEach((h, i) => {
      if (!h) return;
      let val = row[i];
      if (val instanceof Date) val = Utilities.formatDate(val, 'UTC', 'yyyy-MM-dd');
      if (typeof val === 'string' && val.startsWith('[')) {
        try { val = JSON.parse(val); } catch (e) {}
      }
      obj[h] = val === '' ? null : val;
    });
    return obj;
  });
}

/**
 * Read Channels tab
 */
function getChannels(ss) {
  const sheet = ss.getSheetByName('Channels');
  if (!sheet) return [];

  const data = sheet.getDataRange().getValues();
  if (data.length < 2) return [];

  const headers = data[0];
  const rows = data.slice(1).filter(r => r.some(c => c !== ''));

  return rows.map(row => {
    const obj = {};
    headers.forEach((h, i) => {
      if (!h) return;
      let val = row[i];
      if (val instanceof Date) val = val.toISOString();
      obj[h] = val === '' ? null : val;
    });
    return obj;
  });
}

/**
 * Test function — run from script editor to verify
 */
function testBuildResponse() {
  const result = buildResponse();
  Logger.log('Videos count: ' + result.videos.length);
  Logger.log('DailySummary count: ' + result.dailySummary.length);
  Logger.log('Channels count: ' + result.channels.length);
  Logger.log(JSON.stringify(result.videos[0], null, 2));
}
