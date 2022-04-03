import { SearchIcon } from "@chakra-ui/icons";
import {
  Button,
  ButtonGroup,
  FormControl,
  FormLabel,
  HStack,
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

export const phoneRegExp = /^0[1-9]([-. ]?[0-9]{2}){4}$/;

export const validationSchema = Yup.object({
  name: Yup.string().required("Name is required"),
  phone_number: Yup.string().matches(
    phoneRegExp,
    "Must be a valid french phone number."
  ),
  siren: Yup.string()
    .matches(/^[0-9]+$/, "Must be only digits")
    .min(9, "Must be exactly 9 digits")
    .max(9, "Must be exactly 9 digits")
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
  const [fetchingScrapper, setFetchingScrapper] = useState(false);

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
      {(formik, props) => (
        <Form>
          <InputControl mb="10px" name="name" label="Name" />
          <InputControl mb="10px" name="company" label="Company" />
          <InputControl mb="10px" name="phone_number" label="Phone Number" />
          <InputControl mb="10px" name="email" label="Email address" />
          <HStack mb="20px" alignItems="flex-start">
            <InputControl name="siren" label="SIREN number" />
            <FormControl w="">
              <FormLabel></FormLabel>
              <Button
                rightIcon={<SearchIcon />}
                colorScheme="blue"
                variant="outline"
                marginTop="24px"
                isLoading={fetchingScrapper}
                disabled={!(formik.values.siren && !("siren" in formik.errors))}
                onClick={async (values, actions) => {
                  setFetchingScrapper(true);
                  const response = await fetch(
                    `/api/scrapper_company_name/${formik.values.siren}`,
                    {
                      method: "GET",
                      headers: {
                        "Content-Type": "application/json",
                      },
                      body: null,
                    }
                  );

                  if (response.ok) {
                    let company_name = await response.json();
                    toast({
                      title: `Company found: ${company_name}.`,
                      description:
                        "The form has been updated with the company's name.",
                      status: "success",
                      duration: 5000,
                      isClosable: true,
                    });
                    setFetchingScrapper(false);
                    formik.setFieldValue("company", company_name);
                  } else {
                    toast({
                      title: "Siren number invalid or not found.",
                      status: "error",
                      duration: 5000,
                      isClosable: true,
                    });
                    setFetchingScrapper(false);
                  }
                }}
              >
                Search
              </Button>
            </FormControl>
          </HStack>
          <SwitchControl mb="10px" name="called" label="Called" />

          <ButtonGroup mt="30px">
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
