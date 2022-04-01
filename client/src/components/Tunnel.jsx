import { Box, ButtonGroup, Text, useToast } from "@chakra-ui/react";
import { Form, Formik } from "formik";
import {
  InputControl,
  ResetButton,
  SubmitButton,
  SwitchControl,
} from "formik-chakra-ui";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import * as Yup from "yup";

export const Tunnel = () => {
  const [contact, setContact] = useState({});
  const toast = useToast();

  useEffect(() => {
    fetch(`/api/tunnel`)
      .then((response) => {
        if (!response.ok) {
          throw Error(response.statusText);
        }
        return response;
      })
      .then((response) => response.json())
      .then((json) => setContact(json));
  }, []);

  return (
    <Box>
      {Object.keys(contact).length === 0 ? (
        <Text fontSize="1.5em" textAlign="center">
          No more contact to call... <br />
          <Link to="/contacts" style={{ textDecoration: "underline" }}>
            Go add some!
          </Link>
        </Text>
      ) : (
        <>
          <Text fontSize="2em">{contact.name}</Text>
          <Text fontSize="4em">{contact.phone_number}</Text>
          <Formik
            initialValues={contact}
            validateOnMount
            onSubmit={async (values, actions) => {
              const response = await fetch(`/api/tunnel/${contact.id}`, {
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
                  description: "Reloading in 2s.",
                  status: "success",
                  duration: 2000,
                  isClosable: true,
                });
                setTimeout(() => window.location.reload(), 2000);
              }
            }}
            validationSchema={Yup.object({
              siren: Yup.string()
                .matches(/^[0-9]+$/, "Must be only digits")
                .min(14, "Must be exactly 14 digits")
                .max(14, "Must be exactly 14 digits")
                .nullable(),
              called: Yup.boolean().equals(
                [true],
                "Must be checked before submitting."
              ),
            })}
            enableReinitialize
          >
            {(formik, props) => (
              <Form>
                <InputControl name="siren" label="SIREN number" />
                <br />
                <SwitchControl name="called" label="Called" />

                <ButtonGroup mt="40px">
                  <SubmitButton disabled={!(formik.isValid && formik.isValid)}>
                    Submit
                  </SubmitButton>
                  <ResetButton>Reset</ResetButton>
                </ButtonGroup>
              </Form>
            )}
          </Formik>
        </>
      )}
    </Box>
  );
};

export default Tunnel;
