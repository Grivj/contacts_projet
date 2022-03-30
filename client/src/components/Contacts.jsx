import {
  Button,
  Container,
  FormControl,
  FormErrorMessage,
  FormLabel,
  Input,
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalFooter,
  ModalHeader,
  ModalOverlay,
  Table,
  TableContainer,
  Tbody,
  Td,
  Th,
  Thead,
  Tr,
  useDisclosure,
  Center,
} from "@chakra-ui/react";
import { Field, Form, Formik } from "formik";
import { useState } from "react";

const Contacts = () => {
  const [contacts, setContacts] = useState([
    {
      firstName: "John",
      lastName: "Doe",
      company: "Google",
      phoneNumber: "123",
    },
  ]);

  return (
    <Container>
      <CreateContactModal />
      <ContactsTable contacts={contacts} />
    </Container>
  );
};

export const ContactsTable = (contacts) => {
  return (
    <TableContainer>
      <Table>
        <Thead>
          <Tr>
            <Th>Last Name</Th>
            <Th>First Name</Th>
            <Th>Company</Th>
            <Th></Th>
          </Tr>
        </Thead>
        <Tbody>
          {contacts.contacts.length > 0 &&
            contacts.contacts.map((contact, idx) => (
              <Tr key={idx}>
                <Td>{contact.lastName}</Td>
                <Td>{contact.firstName}</Td>
                <Td>{contact.company}</Td>
                <Td>{contact.company}</Td>
              </Tr>
            ))}
          {contacts.contacts.length === 0 && (
            <Tr>
              <Td colSpan={4} textAlign="center">
                No contacts
              </Td>
            </Tr>
          )}
        </Tbody>
      </Table>
    </TableContainer>
  );
};

export const CreateContactModal = () => {
  const { isOpen, onOpen, onClose } = useDisclosure();

  function validateNotEmpty(value) {
    let error;
    if (!value) {
      error = "Field required";
    }
    return error;
  }

  function validatePhoneNumber(value) {
    let error;
    const regex = /^0[1-9]([-. ]?[0-9]{2}){4}$/;
    if (!regex.test(value)) {
      error = "Please enter a valid french phone number";
    }
    return error;
  }
  return (
    <>
      <Center m="20px">
        <Button onClick={onOpen}>Add a contact</Button>
      </Center>
      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Adding a contact</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <Formik
              initialValues={{
                firstName: "",
                lastName: "",
                company: "",
                phoneNumber: "",
              }}
              onSubmit={(values, actions) => {
                setTimeout(() => {
                  alert(JSON.stringify(values, null, 2));
                  actions.setSubmitting(false);
                }, 1000);
              }}
            >
              {(props) => (
                <Form>
                  <Field name="firstName" validate={validateNotEmpty}>
                    {({ field, form }) => (
                      <FormControl
                        isRequired
                        isInvalid={
                          form.errors.firstName && form.touched.firstName
                        }
                      >
                        <FormLabel htmlFor="firstName">First name</FormLabel>
                        <Input
                          {...field}
                          id="firstName"
                          placeholder="First name"
                        />
                        <FormErrorMessage>
                          {form.errors.firstName}
                        </FormErrorMessage>
                      </FormControl>
                    )}
                  </Field>
                  <Field name="lastName" validate={validateNotEmpty}>
                    {({ field, form }) => (
                      <FormControl
                        isRequired
                        isInvalid={
                          form.errors.lastName && form.touched.lastName
                        }
                      >
                        <FormLabel htmlFor="name">Last name</FormLabel>
                        <Input {...field} id="name" placeholder="Last name" />
                        <FormErrorMessage>
                          {form.errors.lastName}
                        </FormErrorMessage>
                      </FormControl>
                    )}
                  </Field>
                  <Field name="company">
                    {({ field, form }) => (
                      <FormControl
                        isInvalid={form.errors.company && form.touched.company}
                      >
                        <FormLabel htmlFor="company">Company</FormLabel>
                        <Input {...field} id="company" placeholder="Company" />
                        <FormErrorMessage>
                          {form.errors.company}
                        </FormErrorMessage>
                      </FormControl>
                    )}
                  </Field>
                  <Field name="phoneNumber" validate={validatePhoneNumber}>
                    {({ field, form }) => (
                      <FormControl
                        isInvalid={
                          form.errors.phoneNumber && form.touched.phoneNumber
                        }
                      >
                        <FormLabel htmlFor="name">Phone number</FormLabel>
                        <Input
                          {...field}
                          id="phoneNumber"
                          placeholder="Phone number"
                        />
                        <FormErrorMessage>
                          {form.errors.phoneNumber}
                        </FormErrorMessage>
                      </FormControl>
                    )}
                  </Field>
                  <ModalFooter>
                    <Button mr={3} onClick={onClose}>
                      Close
                    </Button>
                    <Button
                      colorScheme="blue"
                      isLoading={props.isSubmitting}
                      type="submit"
                    >
                      Submit
                    </Button>
                  </ModalFooter>
                </Form>
              )}
            </Formik>
          </ModalBody>
        </ModalContent>
      </Modal>
    </>
  );
};

export default Contacts;
