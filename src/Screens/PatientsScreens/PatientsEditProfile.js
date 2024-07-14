import React, { useState, createRef, useEffect } from "react";
import {
  StyleSheet,
  TextInput,
  View,
  Text,
  Image,
  KeyboardAvoidingView,
  Keyboard,
  TouchableOpacity,
  ScrollView,
} from "react-native";

import { useSelector, useDispatch } from "react-redux";
import { images, colors } from "../../assets/assets";
import emailValidator from "email-validator";
import { useNavigation } from "@react-navigation/native";
import Axios from "../../Network/axios";
import { currentPatient } from "../../store/slices/patient";
import { setCurrentPatient } from "../../store/slices/patient";
import { defaultToken } from "../../store/slices/token";
import LogoutModal from "../../Components/logoutModal";
import Loader from "../../Components/loader";
import PopUpModal from "../../Components/popUpModal";

const PatientsEditProfile = () => {
  const navigation = useNavigation();
  const patient = useSelector(currentPatient);
  const token = useSelector(defaultToken);
  const dispatch = useDispatch();

  const [logoutVisible, setLogoutVisible] = useState("");
  const [loading, setLoading] = useState(false);

  const [text, setText] = useState("");
  const [error, setError] = useState(false);
  const [modalVisible, setModalVisible] = useState("");

  const [gender,setGender]=useState('');

  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [password1, setPassword1] = useState("");
  const [password2, setPassword2] = useState("");
  const [mobileNumber, setMobileNumber] = useState("");

  const [firstNameText, setFirstNameText] = useState("");
  const [lastNameText, setLastNameText] = useState("");
  const [emailText, setEmailText] = useState("");
  const [mobileText, setMobileText] = useState("");

  const [isPasswordFocused, setIsPasswordFocused] = useState(false);
  const [isPasswordShown, setIsPasswordShown] = useState(true);

  const [passwordValidations, setPasswordValidations] = useState({
    minValueValidation: false,
    numberValidation: false,
    capitalLetterValidation: false,
    specialCharacterValidation: false,
  });

  const handlePasswordChange = (newPassword) => {
    setPassword1(newPassword);
    validatePassword(newPassword);
  };
  const validatePassword = (password) => {
    setPasswordValidations({
      minValueValidation: password.length >= 8,
      numberValidation: /\d/.test(password),
      capitalLetterValidation: /[A-Z]/.test(password),
      specialCharacterValidation: /[^A-Za-z0-9]/.test(password),
    });
  };

  useEffect(() => {
    if (patient) {
      setFirstName(patient.first_name || "");
      setLastName(patient.last_name || "");
      setEmail(patient.email || "");
      setMobileNumber(patient.mobileNumber || "");
      setFirstNameText(patient.first_name || "");
      setLastNameText(patient.last_name || "");
      setEmailText(patient.email || "");
      setMobileText(patient.mobileNumber || "");
      if(patient.gender === 'male'){
        setGender('Male');
    } else{
        setGender('Female');
    }
    }
  }, []);

  const handleSubmitButton = async () => {
    if (!emailValidator.validate(email)) {
      setText("Please enter a valid email address");
      setModalVisible(true);
      setError(true);
      return;
    }

    if (!password1) {
    } else if (password1 !== password2) {
      setText("Passwords do not match");
      setModalVisible(true);
      setError(true);
      return;

    } else {
      validatePassword(password1);
      if (
        !passwordValidations.minValueValidation ||
        !passwordValidations.numberValidation ||
        !passwordValidations.capitalLetterValidation ||
        !passwordValidations.specialCharacterValidation
      ) {
        setText("Password is not valid. Please check the requirements.");
        setModalVisible(true);
        setError(true);
        return;
      }
    }
    if (!/^\d{11}$/.test(mobileNumber)) {
      setText("Please enter a valid 11-digit mobile number");
      setModalVisible(true);
            setError(true);
      return;
    } else if (mobileNumber.charAt(0) !== "0") {
      setText("Mobile Number should start with 0");
      setModalVisible(true);
            setError(true);
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append("first_name", firstName);
    formData.append("last_name", lastName);
    formData.append("mobileNumber", mobileNumber);
    formData.append("email", email);
    formData.append("password1", password1);

    const editResponse = await Axios.patch("/user/edit/", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    console.log("editResponse:", editResponse);
    if (editResponse.status === 200 || editResponse.status === 201) {
      const response = await Axios.get("/user/");
      dispatch(setCurrentPatient(response.data));
      setText('Profile updated successfully ');
      setModalVisible(true);
      setError(false);
    } else {
      setText('Updating Profile Failed, Please try again later.');
      setModalVisible(true);
      setError(true);
    }
    setLoading(false);
  };

  const handleLogoutButton = () => {
    setLogoutVisible(true);
  };

  const handleLogoutResult = (result) => {
    if (result) {
      setLoading(result);
      navigation.navigate("LoginScreen");
    }
  };
  return (
    <View style={styles.mainBody}>
      <View style={styles.upperSection}>
      <LogoutModal logoutVisible={logoutVisible} setLogoutVisible={setLogoutVisible} user={'patient'} setUser={ setCurrentPatient} token = {token} dispatch={dispatch} onLogout={handleLogoutResult}/>
      <PopUpModal modalVisible={modalVisible} setModalVisible={setModalVisible} error={error} text={text}/>
        <Loader loading={loading} />
        <TouchableOpacity
            onPress={handleLogoutButton}
            style={{margin: 20}}>
            <Image source={images.logout} style={{width:40,height:40}}/>
        </TouchableOpacity>
        <View style={styles.profileField}>
          <View style={{ flexDirection: "row" }}>
          {gender === "Male" ? (
            <Image source={images.profileMale} style={{marginLeft: 30, height: 55, width: 55}} />
            ) : gender === "Female" ? (
                <Image source={images.profileFemale} style={{marginLeft: 30, height: 55, width: 55}} />
            ) : <Image source={images.profilePicture} style={{marginLeft: 30, height: 55, width: 55}} />}
            <View
              style={{ flexDirection: "column", marginLeft: 20, marginTop: 5 }}
            >
              <Text
                style={{ fontSize: 18, color: "#C3C9D3", fontWeight: "bold" }}
              >
                Hello,
              </Text>
              {patient &&
              <Text style={styles.profileText}>
                {patient.first_name} {patient.last_name}
              </Text>}
            </View>
          </View>
        </View>
      </View>
      <ScrollView keyboardShouldPersistTaps="handled">
        <KeyboardAvoidingView enabled>
          <View style={styles.lowerSection}>
            <View
              style={{
                backgroundColor: colors.white,
                borderTopRightRadius: 60,
              }}
            >
              <View style={styles.heading}>
                <Image
                  source={images.profileBlue}
                  style={{ width: 30, height: 30 }}
                />
                <Text style={styles.header}>Edit Profile</Text>
              </View>
              <Text style={styles.label}>First Name</Text>
              <View style={styles.inputBar}>
                <Image source={images.user} style={styles.icon} />
                <TextInput
                  style={styles.inputStyle}
                  onChangeText={(text) => setFirstName(text)}
                  underlineColorAndroid="#f000"
                  placeholder={firstNameText}
                  placeholderTextColor="#8b9cb5"
                  autoCapitalize="sentences"
                  returnKeyType="done"
                  onSubmitEditing={Keyboard.dismiss}
                  blurOnSubmit={false}
                />
              </View>
              <Text style={styles.label}>Second Name</Text>
              <View style={styles.inputBar}>
                <Image source={images.user} style={styles.icon} />
                <TextInput
                  style={styles.inputStyle}
                  onChangeText={(SecondName) => setLastName(SecondName)}
                  underlineColorAndroid="#f000"
                  placeholder={lastNameText}
                  placeholderTextColor="#8b9cb5"
                  autoCapitalize="sentences"
                  returnKeyType="done"
                  onSubmitEditing={Keyboard.dismiss}
                  blurOnSubmit={false}
                />
              </View>
              <Text style={styles.label}>Email</Text>
              <View style={styles.inputBar}>
                <Image source={images.mailIcon} style={styles.icon} />
                <TextInput
                  style={styles.inputStyle}
                  onChangeText={(emailtext) => setEmail(emailtext)}
                  underlineColorAndroid="#f000"
                  placeholder={emailText}
                  placeholderTextColor="#8b9cb5"
                  keyboardType="email-address"
                  returnKeyType="done"
                  onSubmitEditing={Keyboard.dismiss}
                  blurOnSubmit={false}
                />
              </View>
              <Text style={styles.label}>Password</Text>
              <View style={styles.inputBar}>
                <Image source={images.passwordIcon} style={styles.icon} />
                <TextInput
                  style={styles.inputStyle}
                  onChangeText={handlePasswordChange}
                  onFocus={() => setIsPasswordFocused(true)}
                  onBlur={() => setIsPasswordFocused(false)}
                  underlineColorAndroid="#f000"
                  returnKeyType="done"
                  secureTextEntry={isPasswordShown}
                  onSubmitEditing={Keyboard.dismiss}
                  blurOnSubmit={false}
                />
                <TouchableOpacity
                  onPress={() => setIsPasswordShown(!isPasswordShown)}
                  style={{ position: "absolute", right: 12 }}
                >
                  {isPasswordShown == false ? (
                    <Image source={images.eyeClosedIcon} style={styles.icon} />
                  ) : (
                    <Image source={images.eyeOpenIcon} style={styles.icon} />
                  )}
                </TouchableOpacity>
              </View>
              {isPasswordFocused && (
                <View>
                  {Object.entries(passwordValidations).map(([key, value]) => (
                    <View
                      key={key}
                      style={{
                        flexDirection: "row",
                        alignItems: "center",
                        marginVertical: -9,
                      }}
                    >
                      {value ? (
                        <Image source={images.right} style={styles.icon} />
                      ) : (
                        <Image source={images.wrong} style={styles.icon} />
                      )}
                      <Text
                        style={{
                          fontSize: 15,
                          fontWeight: "400",
                          color: value ? "#20D56F" : "#C82214",
                          marginLeft: 8,
                        }}
                      >
                        {key === "minValueValidation" &&
                          "Password must be at least 8 Characters"}
                        {key === "numberValidation" &&
                          "Password must have at least one Number"}
                        {key === "capitalLetterValidation" &&
                          "Password must have at least one Capital Letter"}
                        {key === "specialCharacterValidation" &&
                          "Password must have at least one Special Character"}
                      </Text>
                    </View>
                  ))}
                </View>
              )}
              <Text style={styles.label}>Confirm Password</Text>
              <View style={styles.inputBar}>
                <Image source={images.passwordIcon} style={styles.icon} />
                <TextInput
                  style={styles.inputStyle}
                  onChangeText={(ConfirmPassword) =>
                    setPassword2(ConfirmPassword)
                  }
                  underlineColorAndroid="#f000"
                  secureTextEntry={isPasswordShown}
                  returnKeyType="done"
                  onSubmitEditing={Keyboard.dismiss}
                  blurOnSubmit={false}
                />
                <TouchableOpacity
                  onPress={() => setIsPasswordShown(!isPasswordShown)}
                  style={{ position: "absolute", right: 12 }}
                >
                  {isPasswordShown == false ? (
                    <Image source={images.eyeClosedIcon} style={styles.icon} />
                  ) : (
                    <Image source={images.eyeOpenIcon} style={styles.icon} />
                  )}
                </TouchableOpacity>
              </View>
              <Text style={styles.label}>Mobile Number</Text>
              <View style={styles.inputBar}>
                <Image source={images.mobile} style={styles.icon} />
                <TextInput
                  style={styles.inputStyle}
                  onChangeText={(mobileNumber) => setMobileNumber(mobileNumber)}
                  underlineColorAndroid="#f000"
                  placeholder={String(mobileText)}
                  keyboardType="numeric"
                  placeholderTextColor="#8b9cb5"
                  autoCapitalize="none"
                  returnKeyType="done"
                  onSubmitEditing={Keyboard.dismiss}
                  blurOnSubmit={false}
                />
              </View>
              <TouchableOpacity
                style={styles.buttonStyle}
                activeOpacity={0.5}
                onPress={() => {
                  handleSubmitButton();
                }}
              >
                <Text style={styles.buttonTextStyle}>Update</Text>
              </TouchableOpacity>
            </View>
          </View>
        </KeyboardAvoidingView>
      </ScrollView>
      <View style={styles.navBar}>
        <TouchableOpacity
            onPress={() => navigation.navigate('PatientsHomeScreen')}
            style={styles.navBarButton}>
            <Image source={images.home} style={styles.navBarIcon} /> 
        </TouchableOpacity>
        <TouchableOpacity
            onPress={() => navigation.navigate('NewScanScreen')}
            style={styles.cameraButton}>
            <Image source={images.add} style={{width:25,height:25,}} /> 
        </TouchableOpacity>
        <TouchableOpacity
            onPress={() => navigation.navigate('PatientsEditProfile')}
            style={[styles.navBarButton, styles.activeButton]}>
            <Image source={images.profileGreen} style={styles.navBarIcon} /> 
        </TouchableOpacity>
    </View>
    </View>
  );
};
export default PatientsEditProfile;

const styles = StyleSheet.create({
  mainBody: {
    flex: 1,
    backgroundColor: colors.white,
    alignContent: "center",
  },
  upperSection: {
    margin: 0,
    height: 180,
    backgroundColor: colors.darkBlue,
    borderBottomLeftRadius: 60,
  },
  profileField: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginRight: 20,
    marginTop: 10,
  },
  profileText: {
    color: "#C3C9D3",
    fontSize: 16,
  },
  lowerSection: {
    backgroundColor: colors.darkBlue,
    marginBottom: 10,
  },
  heading: {
    flexDirection: "row",
    alignItems: "center",
    marginTop: 30,
    marginLeft: 35,
    marginRight: 35,
    gap: 20,
  },
  header: {
    color: colors.darkBlue,
    fontSize: 20,
    fontWeight: "500",
  },
  label: {
    marginTop: 20,
    marginLeft: 35,
    marginRight: 35,
    color: colors.gray1,
    fontSize: 16,
  },
  inputBar: {
    flexDirection: "row",
    height: 40,
    marginLeft: 35,
    marginRight: 35,
    margin: 10,
    borderWidth: 1,
    borderRadius: 12,
    borderColor: colors.borderColor,
  },
  icon: {
    width: 20,
    height: 20,
    margin: 8,
    marginRight: 10,
    marginLeft: 10,
  },
  inputStyle: {
    flex: 1,
    color: colors.darkBlue,
  },
  buttonStyle: {
    backgroundColor: colors.green,
    color: colors.white,
    width: 350,
    height: 40,
    alignItems: "center",
    borderRadius: 30,
    marginLeft: 35,
    marginRight: 35,
    marginTop: 20,
    marginBottom: 25,
  },
  buttonTextStyle: {
    color: colors.white,
    paddingVertical: 10,
    fontSize: 16,
  },
  navBar: {
    height: 50,
    borderWidth: 1.5,
    borderColor: colors.mintGreen,
    borderTopLeftRadius: 15,
    borderTopRightRadius: 15,
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  navBarButton: {
    borderRadius: 40,
    width: 50,
    height: 50,
    marginLeft: 20,
    marginRight: 20,
    alignItems: "center",
    justifyContent: "center",
    marginTop: 5,
  },
  activeButton: {
    backgroundColor: colors.mintGreen,
  },
  navBarIcon: {
    width: 30,
    height: 30,
    padding: 10,
  },
  cameraButton: {
    backgroundColor: colors.green,
    width: 60,
    height: 60,
    borderRadius: 40,
    borderColor: "#DCDCDC",
    borderTopWidth: 1,
    borderRightWidth: 2,
    borderLeftWidth: 2,
    borderBottomWidth: 5,
    marginBottom: 45,
    alignItems: "center",
    justifyContent: "center",
  },
});