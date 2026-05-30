import React from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  TouchableOpacity,
  Linking,
  Share,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { RouteProp } from '@react-navigation/native';
import { CheckResponse, ClaimResult } from '../services/api';
import VerdictBadge from '../components/VerdictBadge';

type ResultRouteProp = RouteProp<{ Result: { result: CheckResponse } }, 'Result'>;

interface Props {
  route: ResultRouteProp;
}

export default function ResultScreen({ route }: Props) {
  const { result } = route.params;

  const handleShare = async (claim: ClaimResult) => {
    await Share.share({
      message: `GroundTruth factcheck:\n\n"${claim.claim}"\n\nVerdicht: ${claim.verdict.toUpperCase()} (${claim.confidence}% zeker)\n\n${claim.explanation}\n\nDownload GroundTruth voor meer factchecks.`,
    });
  };

  return (
    <SafeAreaView style={styles.container} edges={['bottom']}>
      <ScrollView contentContainerStyle={styles.content}>
        <Text style={styles.originalText} numberOfLines={3}>
          "{result.original_text}"
        </Text>
        {result.cached && (
          <Text style={styles.cachedLabel}>Gecacht resultaat</Text>
        )}

        {result.claims.map((claim, index) => (
          <View key={index} style={styles.claimCard}>
            <Text style={styles.claimLabel}>Bewering {index + 1}</Text>
            <Text style={styles.claimText}>{claim.claim}</Text>

            <VerdictBadge verdict={claim.verdict} confidence={claim.confidence} />

            <Text style={styles.explanation}>{claim.explanation}</Text>

            {claim.sources.length > 0 && (
              <View style={styles.sourcesSection}>
                <Text style={styles.sourcesTitle}>Bronnen</Text>
                {claim.sources.map((source, i) => (
                  <TouchableOpacity
                    key={i}
                    style={styles.sourceRow}
                    onPress={() => Linking.openURL(source.url)}
                  >
                    <Text style={styles.sourceTitle} numberOfLines={1}>
                      {source.title}
                    </Text>
                    <Text style={styles.sourceSnippet} numberOfLines={2}>
                      {source.snippet}
                    </Text>
                  </TouchableOpacity>
                ))}
              </View>
            )}

            <TouchableOpacity style={styles.shareBtn} onPress={() => handleShare(claim)}>
              <Text style={styles.shareBtnText}>Resultaat delen</Text>
            </TouchableOpacity>
          </View>
        ))}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#F9FAFB' },
  content: { padding: 16 },
  originalText: {
    fontSize: 14,
    color: '#6B7280',
    fontStyle: 'italic',
    marginBottom: 4,
    lineHeight: 20,
  },
  cachedLabel: {
    fontSize: 11,
    color: '#0F6E56',
    marginBottom: 12,
  },
  claimCard: {
    backgroundColor: '#fff',
    borderRadius: 14,
    padding: 16,
    marginBottom: 14,
    borderWidth: 1,
    borderColor: '#E5E7EB',
  },
  claimLabel: { fontSize: 11, color: '#9CA3AF', fontWeight: '600', marginBottom: 4 },
  claimText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#111827',
    marginBottom: 12,
    lineHeight: 22,
  },
  explanation: {
    fontSize: 14,
    color: '#374151',
    lineHeight: 21,
    marginTop: 12,
    marginBottom: 16,
  },
  sourcesSection: { borderTopWidth: 1, borderTopColor: '#F3F4F6', paddingTop: 12 },
  sourcesTitle: { fontSize: 12, fontWeight: '600', color: '#6B7280', marginBottom: 8 },
  sourceRow: {
    backgroundColor: '#F9FAFB',
    borderRadius: 8,
    padding: 10,
    marginBottom: 6,
  },
  sourceTitle: { fontSize: 13, color: '#0F6E56', fontWeight: '500' },
  sourceSnippet: { fontSize: 12, color: '#6B7280', marginTop: 2 },
  shareBtn: {
    marginTop: 12,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#D1D5DB',
    paddingVertical: 10,
    alignItems: 'center',
  },
  shareBtnText: { fontSize: 14, color: '#374151', fontWeight: '500' },
});
