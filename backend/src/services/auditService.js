const { analyzeText } = require("./nlpService");
const { analyzeImage } = require("./ocrService");
const { maskPII } = require("../utils/piiMasker");

const Upload = require("../models/Upload");
const Violation = require("../models/Violation");
const AuditLog = require("../models/AuditLog");

const CONFIDENCE_THRESHOLD = 0.8;

const ACTIONS = {
  ALLOW: "ALLOW",
  WARN: "WARN",
  BLOCK: "BLOCK"
};

function decideAction(v) {
  if (v.severity === "HIGH" && v.confidence >= CONFIDENCE_THRESHOLD) {
    return ACTIONS.BLOCK;
  }
  if (v.severity === "MEDIUM") {
    return ACTIONS.WARN;
  }
  return ACTIONS.ALLOW;
}

async function auditContent({ text, image, userId, fileUrl }) {
  let violations = [];
  let inputType = "TEXT";

  if (text && image) inputType = "TEXT_IMAGE";
  else if (image) inputType = "IMAGE";

  const serviceCalls = [];

  if (text) {
    serviceCalls.push(analyzeText(text));
  }

  if (image) {
    serviceCalls.push(analyzeImage(image));
  }

  if (serviceCalls.length > 0) {
    const results = await Promise.all(serviceCalls);
    for (const result of results) {
      violations.push(...(result.violations || []));
    }
  }

  const processed = violations.map(v => ({
    type: v.type,
    severity: v.severity,
    confidence: v.confidence,
    action: decideAction(v),
    maskedText: maskPII(v.type, v.text)
  }));

  let finalAction = ACTIONS.ALLOW;

  if (processed.some(v => v.action === ACTIONS.BLOCK)) {
    finalAction = ACTIONS.BLOCK;
  } else if (processed.some(v => v.action === ACTIONS.WARN)) {
    finalAction = ACTIONS.WARN;
  }

  const upload = await Upload.create({
    user: userId,
    inputType,
    scanMode: "SYNC",
    status: "COMPLETED",
    action: finalAction,
    violationCount: processed.length,
    fileUrl: fileUrl || undefined
  });

  if (processed.length > 0) {
    const violationDocs = processed.map(v => ({
      ...v,
      upload: upload._id
    }));
    await Violation.insertMany(violationDocs);
  }

  await AuditLog.create({
    user: userId,
    action: finalAction,
    upload: upload._id
  });

  return {
    action: finalAction,
    violationCount: processed.length,
    violations: processed
  };
}

module.exports = {
  auditContent
};
