import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

type Verdict = 'waar' | 'onwaar' | 'genuanceerd' | 'onverifieerbaar';

interface Props {
  verdict: Verdict;
  confidence: number;
}

const CONFIG: Record<Verdict, { label: string; bg: string; text: string }> = {
  waar: { label: 'Waar', bg: '#EAF3DE', text: '#27500A' },
  onwaar: { label: 'Onwaar', bg: '#FCEBEB', text: '#791F1F' },
  genuanceerd: { label: 'Genuanceerd', bg: '#FAEEDA', text: '#633806' },
  onverifieerbaar: { label: 'Onverifieerbaar', bg: '#F1EFE8', text: '#444441' },
};

export default function VerdictBadge({ verdict, confidence }: Props) {
  const cfg = CONFIG[verdict] ?? CONFIG.onverifieerbaar;
  return (
    <View style={[styles.badge, { backgroundColor: cfg.bg }]}>
      <Text style={[styles.label, { color: cfg.text }]}>{cfg.label}</Text>
      <Text style={[styles.confidence, { color: cfg.text }]}>{confidence}% zeker</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  badge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    borderRadius: 8,
    paddingHorizontal: 12,
    paddingVertical: 6,
    alignSelf: 'flex-start',
  },
  label: { fontSize: 14, fontWeight: '700' },
  confidence: { fontSize: 12, opacity: 0.8 },
});
