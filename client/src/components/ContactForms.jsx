import {
  Box,
  Button,
  ButtonGroup,
  Center,
  Divider,
  useToast,
} from "@chakra-ui/react";
import { Form, Formik } from "formik";
import {
  InputControl,
  ResetButton,
  SubmitButton,
  SwitchControl,
} from "formik-chakra-ui";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import * as Yup from "yup";
import ContactService from "./ContactService";

const phoneRegExp = /^0[1-9]([-. ]?[0-9]{2}){4}$/;

const validationSchema = Yup.object({
  name: Yup.string().required("Name is required"),
  phone_number: Yup.string().matches(
    phoneRegExp,
    "Must be a valid french phone number."
  ),
  siren: Yup.string()
    .matches(/^[0-9]+$/, "Must be only digits")
    .min(14, "Must be exactly 14 digits")
    .max(14, "Must be exactly 14 digits")
    .nullable(),
  called: Yup.boolean(),
});

export const ModifyContactForm = () => {
  const [contact, setContact] = useState({});
  const { id } = useParams();
  const navigate = useNavigate();

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
      .catch((error) => window.alert(error))
      .then(() => navigate("/contacts"));
  };

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
          <InputControl name="name" label="Name" />
          <InputControl name="company" label="Company" />
          <InputControl name="phone_number" label="Phone number" />
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

export const NewContactForm = ({ onNewContact }) => {
  const toast = useToast();

  return (
    <Formik
      initialValues={{
        name: "",
        company: "",
        phone_number: "",
      }}
      onSubmit={async (values, actions) => {
        const response = await fetch("/api/contacts", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(values),
        }).then();

        if (response.ok) {
          onNewContact(response.json());
          actions.setSubmitting(false);
          actions.resetForm();
          toast({
            title: "Contact created.",
            status: "success",
            duration: 5000,
            isClosable: true,
          });
        }
      }}
      validationSchema={validationSchema}
      enableReinitialize
    >
      {(props) => (
        <Form>
          <InputControl name="name" label="Name" />
          <InputControl name="company" label="Company" />
          <InputControl name="phone_number" label="Phone Number" />

          <ButtonGroup mt="10px">
            <SubmitButton>Submit</SubmitButton>
            <ResetButton>Reset</ResetButton>
          </ButtonGroup>
        </Form>
      )}
    </Formik>
  );
};

export const UpdateContactForm = () => {
  const [contact, setContact] = useState({});
  const { id } = useParams();
  const toast = useToast();

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

  return (
    <Formik
      initialValues={contact}
      onSubmit={async (values, actions) => {
        const response = await fetch(`/api/contacts/${id}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(values),
        }).then();

        if (response.ok) {
          actions.setSubmitting(false);
          toast({
            title: "Contact updated.",
            status: "success",
            duration: 5000,
            isClosable: true,
          });
        }
      }}
      validationSchema={validationSchema}
      enableReinitialize
    >
      {(props) => (
        <Form>
          <InputControl name="name" label="Name" />
          <InputControl name="company" label="Company" />
          <InputControl name="phone_number" label="Phone Number" />
          <InputControl name="email" label="Email address" />
          <InputControl name="siren" label="SIREN number" />
          <SwitchControl name="called" label="Called" />

          <ButtonGroup mt="10px">
            <SubmitButton>Submit</SubmitButton>
            <ResetButton>Reset</ResetButton>
          </ButtonGroup>
        </Form>
      )}
    </Formik>
  );
};
