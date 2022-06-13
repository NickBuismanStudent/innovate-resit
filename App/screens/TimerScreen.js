import { View, Text } from "../components/Themed";
import { StyleSheet, Pressable } from "react-native";
import Colors from '../constants/Colors';
import { useState } from "react";
import { Settings } from "react-native";
import TimerText from "../components/TimerText";

export function TimerScreen({navigation}) {
    const [time, setTime] = useState(Settings['focus-time'] * 60);

    return (
        <View style={Styles.OuterContainer}>
          <View style={Styles.InnerContainer}>
            <View style={Styles.TitleContainer}>
              <Text style={Styles.SectionTitle}>Pomodoro Timer</Text>
              <Pressable>
                <Text style={Styles.SettingsButton}>Settings</Text>
              </Pressable>
            </View>
            <View style={Styles.TimerContainer}>
              <TimerText time={time} />
              {/* <ControlButtons func={setTime} /> */}
            </View>
            <View>
              <Text style={Styles.TasksText}>No tasks available yet.</Text>
            </View>
          </View>
        </View>
    );
}

const Styles = StyleSheet.create({
  OuterContainer: {
    alignItems: 'center',
  },
  InnerContainer: {
    width: '80%',
    marginVertical: 20,
    alignItems: 'center',
  },
  TitleContainer: {
    width: '100%',
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  SectionTitle: {
    color: Colors.light.textColorBlack,
    fontSize: 22,
    fontWeight: '700',
  },
  SettingsButton: {
    color: Colors.light.colorBlue900,
    textDecorationLine: 'underline',
    textDecorationColor: Colors.light.colorBlue900,
  },
  TimerContainer: {
    marginVertical: 20,
  },
  TasksText: {
    color: Colors.light.colorGray800,
  },
});