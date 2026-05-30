import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  FlatList,
  TouchableOpacity,
  StyleSheet,
  Alert,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { StackNavigationProp } from '@react-navigation/stack';
import { RootStackParamList } from '../../App';
import { CheckResponse } from '../services/api';
import { getHistory, clearHistory } from '../services/storage';
import VerdictBadge from '../components/VerdictBadge';

type HistoryNavigationProp = StackNavigationProp<RootStackParamList, 'History'>;

interface Props {
  navigation: HistoryNavigationProp;
}

export default function HistoryScreen({ navigation }: Props) {
  const [history, setHistory] = useState<CheckResponse[]>([]);

  useEffect(() => {
    getHistory().then(setHistory);
  }, []);

  const handleClear = () => {
    Alert.alert('Geschiedenis wissen', 'Ben je zeker?', [
      { text: 'Annuleren', style: 'cancel' },
      {
        text: 'Wissen',
        style: 'destructive',
        onPress: async () => {
          await clearHistory();
          setHistory([]);
        },
      },
    ]);
  };

  if (history.length === 0) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.empty}>
          <Text style={styles.emptyText}>Nog geen factchecks uitgevoerd.</Text>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container} edges={['bottom']}>
      <FlatList
        data={history}
        keyExtractor={(item) => item.id}
        contentContainerStyle={styles.list}
        ListHeaderComponent={
          <TouchableOpacity style={styles.clearBtn} onPress={handleClear}>
            <Text style={styles.clearBtnText}>Geschiedenis wissen</Text>
          </TouchableOpacity>
        }
        renderItem={({ item }) => (
          <TouchableOpacity
            style={styles.card}
            onPress={() => (navigation as any).navigate('Result', { result: item })}
          >
            <Text style={styles.cardText} numberOfLines={2}>
              {item.original_text}
            </Text>
            {item.claims[0] && (
              <View style={styles.badgeRow}>
                <VerdictBadge
                  verdict={item.claims[0].verdict}
                  confidence={item.claims[0].confidence}
                />
              </View>
            )}
            <Text style={styles.dateText}>
              {new Date(item.created_at).toLocaleDateString('nl-BE')}
            </Text>
          </TouchableOpacity>
        )}
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#F9FAFB' },
  empty: { flex: 1, alignItems: 'center', justifyContent: 'center' },
  emptyText: { color: '#9CA3AF', fontSize: 15 },
  list: { padding: 16 },
  clearBtn: { alignSelf: 'flex-end', marginBottom: 12 },
  clearBtnText: { fontSize: 13, color: '#DC2626' },
  card: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 14,
    marginBottom: 10,
    borderWidth: 1,
    borderColor: '#E5E7EB',
  },
  cardText: { fontSize: 14, color: '#111827', marginBottom: 8, lineHeight: 20 },
  badgeRow: { marginBottom: 6 },
  dateText: { fontSize: 11, color: '#9CA3AF' },
});
