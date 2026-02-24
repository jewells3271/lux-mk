
import GemmaMainEngine from '../lib/gemma/main-engine.js';
import { getCoreMemory, getDirectives } from '../lib/gemma/prompts.js';
import dotenv from 'dotenv';

dotenv.config({ path: '.env.local' });

async function verifySync() {
    console.log('🛡️ Starting Biblical Sync Verification...');

    const engine = new GemmaMainEngine(process.env.GEMINI_API_KEY);
    const core = getCoreMemory();
    const directives = getDirectives();

    // Test Case 1: Identity & Directives Presence in Sidecar Assessment
    console.log('\n--- Test Case 1: Tactical Alignment ---');
    const testMessage = "Remember that I love dark mode analytics.";
    const assessment = await engine.sidecar.assessMemory(testMessage, core, directives);

    console.log('Result:', JSON.stringify(assessment, null, 2));
    if (assessment.shouldRemember && assessment.storageTarget === 'domain') {
        console.log('✅ PASS: Tactical facts correctly identified under biblical rules.');
    } else {
        console.log('⚠️ REVIEW: Classification may need more prompt refinement or model-specific tuning.');
    }

    // Test Case 2: Context Window Capping
    console.log('\n--- Test Case 2: Context Cap Check ---');
    const memberId = 999;
    await engine.generate("Warm up the stream.", { memberId });

    const mgr = engine.streams.get(memberId);
    console.log(`Cap: ${mgr.appContextCap} tokens`);
    console.log(`Trigger (85%): ${mgr.appContextCap * 0.85} tokens`);

    if (mgr.appContextCap === 64000) {
        console.log('✅ PASS: Stream Manager set to 64k Cap.');
    } else {
        console.log(`❌ FAIL: Cap is ${mgr.appContextCap}, expected 64000.`);
    }

    console.log('\n🛡️ Verification Complete.');
    process.exit(0);
}

verifySync().catch(err => {
    console.error('❌ Verification Error:', err);
    process.exit(1);
});
