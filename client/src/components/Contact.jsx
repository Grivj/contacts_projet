import { Box, Button, ButtonGroup, Center, Divider } from "@chakra-ui/react";
import { Formik } from "formik";
import {
  InputControl,
  ResetButton,
  SubmitButton,
  SwitchControl,
} from "formik-chakra-ui";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import * as Yup from "yup";
import ContactService from "./ContactService";

const ModifyContactForm = ({ mode }) => {
  const [contact, setContact] = useState({});
  const { id } = useParams();

  useEffect(() => {
    fetch(`/api/contacts/${id}`)
      .then((response) => {
        if (!response.ok) {
          throw Error(response.statusText);
        }
        return response;
      })
      .then((response) => response.json())
      .then((json) => setContact(json))
      .catch((error) => console.error(error));
  }, [id]);

  const onSubmit = (values) => {
    setContact(values);
    console.log(contact);
    ContactService.updateContact(JSON.stringify(values, null, 2), id)
      .then(() => window.alert("Contact was successfully updated"))
      .catch((error) => window.alert(error));
  };

  const handleDelete = () => {
    ContactService.deleteContact(id)
      .then(() => window.alert("Contact was successfully deleted"))
      .catch((error) => window.alert(error));
  };

  const phoneRegExp = /^0[1-9]([-. ]?[0-9]{2}){4}$/;

  const validationSchema = Yup.object({
    firstName: Yup.string("First name should be a string").required(
      "First name is required"
    ),
    lastName: Yup.string().required("Last name is required"),
    phoneNumber: Yup.string().matches(
      phoneRegExp,
      "Must be a valid french phone number."
    ),
    siren: Yup.string()
      .matches(/^[0-9]+$/, "Must be only digits")
      .min(14, "Must be exactly 14 digits")
      .max(14, "Must be exactly 14 digits"),
    called: Yup.boolean(),
  });
  return (
    <Formik
      initialValues={contact}
      onSubmit={onSubmit}
      validationSchema={validationSchema}
      enableReinitialize
    >
      {({ handleSubmit, values, errors }) => (
        <Box
          borderWidth="1px"
          rounded="lg"
          as="form"
          p={6}
          onSubmit={handleSubmit}
        >
          <InputControl name="name" label="First Name" />
          <InputControl name="company" label="Company" />
          <InputControl name="phone_number" label="Phone Number" />
          <InputControl name="siren" label="SIREN" />
          <SwitchControl name="called" label="Called" />

          <ButtonGroup mt="10px">
            <SubmitButton>Submit</SubmitButton>
            <ResetButton>Reset</ResetButton>
            <Center>
              <Divider m="20px" orientation="vertical" />
            </Center>
            <Button colorScheme="red" variant="solid" onClick={handleDelete}>
              Delete
            </Button>
          </ButtonGroup>
        </Box>
      )}
    </Formik>
  );
};

export default ModifyContactForm;
