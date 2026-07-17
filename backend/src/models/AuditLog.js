const mongoose = require("mongoose");

const auditLogSchema = new mongoose.Schema(
  {
    user: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "User"
    },

    action: {
      type: String,
      required: true
    },

    upload: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "Upload"
    },

    meta: {
      type: Object
    }
  },
  { timestamps: true }
);

module.exports = mongoose.model("AuditLog", auditLogSchema);
