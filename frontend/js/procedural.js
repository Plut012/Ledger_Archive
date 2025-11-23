// Procedural Generation Utilities
// Used for creating the illusion of vast historical data

/**
 * Seeded random number generator (Mulberry32)
 * Same seed = same sequence of random numbers
 */
class SeededRandom {
    constructor(seed) {
        this.seed = seed;
    }

    next() {
        let t = this.seed += 0x6D2B79F5;
        t = Math.imul(t ^ t >>> 15, t | 1);
        t ^= t + Math.imul(t ^ t >>> 7, t | 61);
        return ((t ^ t >>> 14) >>> 0) / 4294967296;
    }

    nextInt(min, max) {
        return Math.floor(this.next() * (max - min + 1)) + min;
    }

    nextFloat(min, max) {
        return this.next() * (max - min) + min;
    }

    choice(array) {
        return array[this.nextInt(0, array.length - 1)];
    }
}

/**
 * Procedural Block Generator
 * Generates consistent "historical" blocks based on index
 */
const ProceduralChain = {
    // Constants for generation
    GENESIS_TIME: 1704067200000, // Jan 1, 2024
    AVG_BLOCK_TIME: 600000, // 10 minutes in ms
    DIFFICULTY_PREFIX: '0000', // 4 leading zeros
    MASTER_SEED: 8472934, // Imperium master seed

    /**
     * Generate a historical block procedurally
     */
    generateBlock(index) {
        const rng = new SeededRandom(this.MASTER_SEED + index);

        // Timestamp increases linearly
        const timestamp = this.GENESIS_TIME + (index * this.AVG_BLOCK_TIME);
        const date = new Date(timestamp);
        const timestampStr = date.toISOString();

        // Generate realistic-looking hash
        const hash = this.generateHash(index, rng);
        const previousHash = index === 0
            ? '0'.repeat(64)
            : this.generateHash(index - 1, new SeededRandom(this.MASTER_SEED + index - 1));

        // Random nonce
        const nonce = rng.nextInt(0, 1000000);

        // Random number of transactions (0-5)
        const txCount = rng.nextInt(0, 5);
        const transactions = [];

        for (let i = 0; i < txCount; i++) {
            transactions.push(this.generateTransaction(index, i, rng));
        }

        return {
            index,
            timestamp: timestampStr,
            hash,
            previous_hash: previousHash,
            nonce,
            transactions,
            is_procedural: true // Mark as procedurally generated
        };
    },

    /**
     * Generate a realistic-looking transaction
     */
    generateTransaction(blockIndex, txIndex, rng) {
        const isCoinbase = txIndex === 0 && rng.next() < 0.3; // 30% chance first tx is coinbase

        if (isCoinbase) {
            return {
                sender: 'COINBASE',
                recipient: this.generateAddress(rng),
                amount: 50,
                is_coinbase: true,
                timestamp: Date.now(),
                signature: 'COINBASE'
            };
        }

        return {
            sender: this.generateAddress(rng),
            recipient: this.generateAddress(rng),
            amount: rng.nextInt(1, 100),
            is_coinbase: false,
            timestamp: Date.now(),
            signature: this.generateSignature(rng)
        };
    },

    /**
     * Generate a realistic hash with proper difficulty
     */
    generateHash(index, rng) {
        const chars = '0123456789abcdef';
        let hash = this.DIFFICULTY_PREFIX; // Start with difficulty prefix

        // Generate rest of hash (64 chars total)
        for (let i = this.DIFFICULTY_PREFIX.length; i < 64; i++) {
            hash += chars[rng.nextInt(0, 15)];
        }

        return hash;
    },

    /**
     * Generate a realistic address
     */
    generateAddress(rng) {
        const chars = '0123456789abcdef';
        let addr = '';
        for (let i = 0; i < 40; i++) {
            addr += chars[rng.nextInt(0, 15)];
        }
        return addr;
    },

    /**
     * Generate a realistic signature
     */
    generateSignature(rng) {
        const chars = '0123456789abcdef';
        let sig = '';
        for (let i = 0; i < 128; i++) {
            sig += chars[rng.nextInt(0, 15)];
        }
        return sig;
    }
};

/**
 * Procedural Network Generator
 * Generates node names and metadata for vast network
 */
const ProceduralNetwork = {
    SECTOR_PREFIXES: ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon', 'Zeta', 'Eta', 'Theta'],
    STATION_TYPES: ['Archive', 'Relay', 'Hub', 'Outpost', 'Citadel'],
    CELESTIAL_NAMES: [
        'Proxima', 'Sirius', 'Vega', 'Altair', 'Deneb', 'Rigel', 'Betelgeuse',
        'Antares', 'Arcturus', 'Capella', 'Pollux', 'Aldebaran', 'Spica',
        'Regulus', 'Canopus', 'Achernar', 'Bellatrix', 'Mintaka', 'Alnilam',
        'Alnitak', 'Saiph', 'Alnair', 'Alioth', 'Alkaid', 'Mizar', 'Dubhe'
    ],

    /**
     * Generate a procedural node name
     */
    generateNodeName(index, rng) {
        const sector = this.SECTOR_PREFIXES[index % this.SECTOR_PREFIXES.length];
        const celestial = rng.choice(this.CELESTIAL_NAMES);
        const type = rng.choice(this.STATION_TYPES);
        const suffix = rng.nextInt(1, 99);

        return `${sector} ${celestial} ${type}-${suffix}`;
    },

    /**
     * Generate node tier (1=Core, 2=Sector, 3=Frontier)
     */
    getNodeTier(index) {
        if (index < 5) return 1; // Core
        if (index < 15) return 2; // Sector
        return 3; // Frontier
    }
};
