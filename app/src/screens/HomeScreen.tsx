import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  ActivityIndicator,
  StyleSheet,
  Alert,
  ScrollView,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import * as ImagePicker from 'expo-image-picker';
import { StackNavigationProp } from '@react-navigation/stack';
import { RootStackParamList } from '../../App';
import { checkText, CheckResponse } from '../services/api';
import { saveToHistory } from '../services/storage';

type HomeScreenNavigationProp = StackNavigationProp<RootStackParamList, 'Home'>;

interface Props {
  navigation: HomeScreenNavigationProp;
}

export default function HomeScreen({ navigation }: Props) {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);

  const handleCheck = async (inputText: string, imageBase64?: string) => {
    if (!inputText.trim() && !imageBase64) return;
    setLoading(true);
    try {
      const result: CheckResponse = await checkText(inputText, undefined, imageBase64);
      await saveToHistory(result);
      navigation.navigate('Result', { checkId: result.id });
      // Pass result via navigation state for simplicity
      (navigation as any).navigate('Result', { result });
    } catch (e: any) {
      Alert.alert('Fout', e.message || 'Er is iets misgegaan.');
    } finally {
      setLoading(false);
    }
  };

  const pickImage = async () => {
    const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert('Geen toegang', 'Geef toegang tot je foto\'s om screenshots te analyseren.');
      return;
    }
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      base64: true,
      quality: 0.8,
    });
    if (!result.canceled && result.assets[0].base64) {
      handleCheck('', result.assets[0].base64);
    }
  };

  return (
    <SafeAreaView style={styles.container} edges={['bottom']}>
      <ScrollView contentContainerStyle={styles.content} keyboardShouldPersistTaps="handled">
        <Text style={styles.headline}>Wat wil je checken?</Text>
        <Text style={styles.sub}>Plak een tekst, tweet, of nieuwsbericht hieronder.</Text>

        <TextInput
          style={styles.input}
          multiline
          numberOfLines={6}
          placeholder="Plak hier je tekst of bewering..."
          placeholderTextColor="#9CA3AF"
          value={text}
          onChangeText={setText}
          textAlignVertical="top"
        />

        <TouchableOpacity
          style={[styles.btnPrimary, (!text.trim() || loading) && styles.btnDisabled]}
          onPress={() => handleCheck(text)}
          disabled={!text.trim() || loading}
        >
          {loading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.btnPrimaryText}>Factcheck uitvoeren</Text>
          )}
        </TouchableOpacity>

        <TouchableOpacity style={styles.btnSecondary} onPress={pickImage} disabled={loading}>
          <Text style={styles.btnSecondaryText}>Screenshot uploaden</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.historyLink}
          onPress={() => navigation.navigate('History')}
        >
          <Text style={styles.historyLinkText}>Mijn geschiedenis bekijken</Text>
        </TouchableOpacity>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#F9FAFB' },
  content: { padding: 20, paddingTop: 32 },
  headline: { fontSize: 26, fontWeight: '700', color: '#111827', marginBottom: 6 },
  sub: { fontSize: 15, color: '#6B7280', marginBottom: 24 },
  input: {
    backgroundColor: '#fff',
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#E5E7EB',
    padding: 14,
    fontSize: 15,
    color: '#111827',
    minHeight: 140,
    marginBottom: 16,
  },
  btnPrimary: {
    backgroundColor: '#0F6E56',
    borderRadius: 12,
    paddingVertical: 15,
    alignItems: 'center',
    marginBottom: 12,
  },
  btnDisabled: { backgroundColor: '#9CA3AF' },
  btnPrimaryText: { color: '#fff', fontSize: 16, fontWeight: '600' },
  btnSecondary: {
    backgroundColor: '#fff',
    borderRadius: 12,
    paddingVertical: 14,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#D1D5DB',
    marginBottom: 24,
  },
  btnSecondaryText: { color: '#374151', fontSize: 15, fontWeight: '500' },
  historyLink: { alignItems: 'center', paddingVertical: 8 },
  historyLinkText: { color: '#0F6E56', fontSize: 14 },
});
