// violation model

const mongoose = require("mongoose");

const violationSchema = new mongoose.Schema(
  {
    upload: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "Upload",
      required: true
    },

    type: {
      type: String,
      required: true
    },

    severity: {
      type: String,
      enum: ["LOW", "MEDIUM", "HIGH"],
      required: true
    },

    confidence: {
      type: Number,
      required: true
    },

    action: {
      type: String,
      enum: ["ALLOW", "WARN", "BLOCK"],
      required: true
    },

    maskedText: {
      type: String,
      required: true
    }
  },
  { timestamps: true }
);

module.exports = mongoose.model("Violation", violationSchema);
