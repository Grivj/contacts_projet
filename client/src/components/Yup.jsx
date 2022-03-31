import { Box, ButtonGroup } from "@chakra-ui/react";
import { Formik } from "formik";
import {
  InputControl,
  PercentComplete,
  ResetButton,
  SubmitButton,
} from "formik-chakra-ui";
import * as Yup from "yup";

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

const onSubmit = (values) => {
  sleep(300).then(() => {
    window.alert(JSON.stringify(values, null, 2));
  });
};

const phoneRegExp = /^0[1-9]([-. ]?[0-9]{2}){4}$/;

const initialValues = {
  firstName: "",
  lastName: "",
  company: "",
  phoneNumber: "",
  siren: "",
};
const validationSchema = Yup.object({
  firstName: Yup.string("First name should be a string").required(
    "First name is required"
  ),
  lastName: Yup.string().required("Last name is required"),
  phoneNumber: Yup.string().matches(phoneRegExp, "Phone number is not valid, only digits and of length 10"),
  siren: Yup.string()
    .matches(/^[0-9]+$/, "Must be only digits")
    .min(14, "Must be exactly 14 digits")
    .max(14, "Must be exactly 14 digits"),
});

const FormL = () => {
  return (
    <Formik
      initialValues={initialValues}
      onSubmit={onSubmit}
      validationSchema={validationSchema}
    >
      {({ handleSubmit, values, errors }) => (
        <Box
          borderWidth="1px"
          rounded="lg"
          shadow="1px 1px 3px rgba(0,0,0,0.3)"
          maxWidth={800}
          p={6}
          m="10px auto"
          as="form"
          onSubmit={handleSubmit}
        >
          <InputControl name="firstName" label="First Name"/>
          <InputControl name="lastName" label="Last Name" />
          <InputControl name="company" label="Company" />
          <InputControl name="phoneNumber" label="Phone Number" />
          <InputControl name="siren" label="SIREN" />

          <PercentComplete />
          <ButtonGroup>
            <SubmitButton>Submit</SubmitButton>
            <ResetButton>Reset</ResetButton>
          </ButtonGroup>

          <Box as="pre" marginY={10}>
            {JSON.stringify(values, null, 2)}
            <br />
            {JSON.stringify(errors, null, 2)}
          </Box>
        </Box>
      )}
    </Formik>
  );
};

export default FormL;
