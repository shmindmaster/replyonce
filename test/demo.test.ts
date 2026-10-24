import { expect, it } from 'vitest';
import { runDemo } from '../src/demo.js';
import { eachStore } from './helpers.js';

// CI sets this to run each seed several times: timing differs per run, so a rare
// interleaving that a single pass misses shows up across repeats.
const repeat = Math.max(1, Number(process.env.REPLYONCE_DEMO_REPEAT ?? 1));

eachStore('chaos demo', (makeStore, name) => {
  const conversations = name === 'memory' ? 200 : 60;
  for (const seed of [1, 2, 3]) {
    for (let i = 1; i <= repeat; i++) {
      const label = repeat > 1 ? ` (pass ${i}/${repeat})` : '';
      it(`seed ${seed}${label}: no customer message answered twice, none left unanswered`, async () => {
        const report = await runDemo({ conversations, seed, store: await makeStore() });
        expect(report.without.duplicateAnswers).toBeGreaterThan(0);
        expect(report.with.duplicateAnswers).toBe(0);
        expect(report.with.unanswered).toBe(0);
      });
    }
  }
});
