import { expect, it } from 'vitest';
import { runDemo } from '../src/demo.js';
import { eachStore } from './helpers.js';

eachStore('chaos demo', (makeStore, name) => {
  const conversations = name === 'memory' ? 200 : 60;
  for (const seed of [1, 2, 3]) {
    it(`seed ${seed}: no customer message answered twice, none left unanswered`, async () => {
      const report = await runDemo({ conversations, seed, store: await makeStore() });
      expect(report.without.duplicateAnswers).toBeGreaterThan(0);
      expect(report.with.duplicateAnswers).toBe(0);
      expect(report.with.unanswered).toBe(0);
    });
  }
});
