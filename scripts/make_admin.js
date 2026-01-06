const mongoose = require('../backend/node_modules/mongoose');
const dotenv = require('../backend/node_modules/dotenv');
const User = require('../backend/src/models/User');
const connectDB = require('../backend/src/config/db');

dotenv.config({ path: '../backend/.env' });

const makeAdmin = async () => {
    await connectDB();

    const email = process.argv[2];

    if (!email) {
        console.log('Please provide an email: node make_admin.js <email>');
        process.exit(1);
    }

    try {
        const user = await User.findOne({ email });

        if (!user) {
            console.log('User not found');
            process.exit(1);
        }

        user.role = 'admin';
        await user.save();

        console.log(`Success! User ${user.name} (${user.email}) is now an Admin.`);
        process.exit();
    } catch (error) {
        console.error(error);
        process.exit(1);
    }
};

makeAdmin();
