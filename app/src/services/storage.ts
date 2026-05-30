import * as SecureStore from 'expo-secure-store';
import { CheckResponse } from './api';

const HISTORY_KEY = 'groundtruth_history';
const MAX_HISTORY = 50;

export async function saveToHistory(result: CheckResponse): Promise<void> {
  try {
    const history = await getHistory();
    const updated = [result, ...history].slice(0, MAX_HISTORY);
    await SecureStore.setItemAsync(HISTORY_KEY, JSON.stringify(updated));
  } catch (e) {
    console.warn('Could not save history:', e);
  }
}

export async function getHistory(): Promise<CheckResponse[]> {
  try {
    const raw = await SecureStore.getItemAsync(HISTORY_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch (e) {
    return [];
  }
}

export async function clearHistory(): Promise<void> {
  await SecureStore.deleteItemAsync(HISTORY_KEY);
}
