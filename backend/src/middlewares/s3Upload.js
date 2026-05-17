const { S3Client, PutObjectCommand } = require("@aws-sdk/client-s3");

const s3Client = new S3Client({
    region: process.env.AWS_REGION,
    credentials: {
        accessKeyId: process.env.AWS_ACCESS_KEY_ID,
        secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
    },
});

/**
 * Uploads a file buffer to S3
 * @param {Buffer} fileBuffer - The file content
 * @param {string} mimeType - The file mime type
 * @param {string} originalName - Original filename to extract extension
 * @returns {Promise<string>} - The S3 object URL
 */
async function uploadToS3(fileBuffer, mimeType, originalName) {
    const fileExt = originalName.split('.').pop();
    const fileName = `${Date.now()}-${Math.round(Math.random() * 1E9)}.${fileExt}`;

    const command = new PutObjectCommand({
        Bucket: process.env.AWS_S3_BUCKET_NAME,
        Key: fileName,
        Body: fileBuffer,
        ContentType: mimeType,
    });

    await s3Client.send(command);

    // Return the URL (assuming standard S3 URL format)
    return `https://${process.env.AWS_S3_BUCKET_NAME}.s3.${process.env.AWS_REGION}.amazonaws.com/${fileName}`;
}

async function uploadTextToS3(text, originalName = "content.txt") {
    const fileExt = originalName.split('.').pop() || "txt";
    const fileName = `${Date.now()}-${Math.round(Math.random() * 1E9)}.${fileExt}`;

    const command = new PutObjectCommand({
        Bucket: process.env.AWS_S3_BUCKET_NAME,
        Key: fileName,
        Body: text,
        ContentType: "text/plain",
    });

    await s3Client.send(command);

    return `https://${process.env.AWS_S3_BUCKET_NAME}.s3.${process.env.AWS_REGION}.amazonaws.com/${fileName}`;
}

module.exports = { uploadToS3, uploadTextToS3 };
