import { Button, ButtonGroup, useToast } from "@chakra-ui/react";
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

const phoneRegExp = /^0[1-9]([-. ]?[0-9]{2}){4}$/;

const validationSchema = Yup.object({
  name: Yup.string().required("Name is required"),
  phone_number: Yup.string().matches(
    phoneRegExp,
    "Must be a valid french phone number."
  ),
  siren: Yup.string()
    .matches(/^[0-9]+$/, "Must be only digits")
    .min(9, "Must be exactly 14 digits")
    .max(9, "Must be exactly 14 digits")
    .nullable(),
  called: Yup.boolean(),
});

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
          onNewContact(await response.json());
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
  const navigate = useNavigate();
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
            <Button
              colorScheme="red"
              variant="solid"
              onClick={async (values, actions) => {
                const response = await fetch(`/api/contacts/${id}`, {
                  method: "DELETE",
                  headers: {
                    "Content-Type": "application/json",
                  },
                  body: null,
                }).then();

                if (response.ok) {
                  toast({
                    title: "Contact deleted.",
                    status: "success",
                    duration: 5000,
                    isClosable: true,
                  });
                  navigate("/contacts");
                }
              }}
            >
              Delete
            </Button>
          </ButtonGroup>
        </Form>
      )}
    </Formik>
  );
};
