#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

// Minimal CLI parsing
const args = process.argv.slice(2);
const parsed = {};
for (let i = 0; i < args.length; i++) {
  const a = args[i];
  if (a.startsWith('--')) {
    const key = a.slice(2);
    const next = args[i+1];
    if (next && !next.startsWith('--')) {
      parsed[key] = next;
      i++;
    } else {
      parsed[key] = true;
    }
  }
}

const actor = parsed.actor || 'assistant';
const action = parsed.action || 'note';
const message = parsed.message || '';
let meta = parsed.meta || null;

try {
  if (meta) meta = JSON.parse(meta);
} catch (e) {
  console.error('Failed to parse --meta JSON:', e.message);
  process.exit(2);
}

const logPath = path.resolve(__dirname, '..', 'www', 'assistant_log.json');

function readLog() {
  try {
    if (!fs.existsSync(logPath)) return [];
    const raw = fs.readFileSync(logPath, 'utf8') || '[]';
    return JSON.parse(raw);
  } catch (e) {
    console.error('Error reading log:', e.message);
    return [];
  }
}

function writeLog(arr) {
  try {
    fs.mkdirSync(path.dirname(logPath), { recursive: true });
    fs.writeFileSync(logPath, JSON.stringify(arr, null, 2), 'utf8');
  } catch (e) {
    console.error('Error writing log:', e.message);
    process.exit(3);
  }
}

const logs = readLog();
const entry = {
  ts: new Date().toISOString(),
  actor,
  action,
  message,
  meta: meta || null
};

logs.push(entry);
writeLog(logs);
console.log('Appended log entry:', entry);
