import { CheckIcon, CloseIcon, SearchIcon } from "@chakra-ui/icons";
import {
  Container,
  Link,
  Table,
  Tbody,
  Td,
  Th,
  Thead,
  Tr,
} from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { NewContactForm } from "./ContactForms";

const Contacts = () => {
  const [contacts, setContacts] = useState([]);

  useEffect(() => {
    fetch("/api/contacts")
      .then((response) => response.json())
      .then((json) => setContacts(json));
  }, []);

  return (
    <Container>
      <NewContactForm
        onNewContact={(contact) =>
          setContacts((currentContacts) => [...currentContacts, contact])
        }
      />
      <ContactsTable contacts={contacts} />
    </Container>
  );
};

export const ContactsTable = (contacts) => {
  return (
    <Table>
      <Thead>
        <Tr>
          <Th>Name</Th>
          <Th>Company</Th>
          <Th>Called</Th>
          <Th></Th>
        </Tr>
      </Thead>
      <Tbody>
        {contacts.contacts.length > 0 &&
          contacts.contacts.map((contact, idx) => (
            <Tr key={idx}>
              <Td>{contact.name ? contact.name : "-"}</Td>
              <Td>{contact.company ? contact.company : "-"}</Td>
              <Td>
                {contact.called ? (
                  <CheckIcon color="green" />
                ) : (
                  <CloseIcon color="red" />
                )}
              </Td>
              <Td>
                <Link href={`/contacts/${contact.id}`}>
                  <SearchIcon />
                </Link>
              </Td>
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
  );
};

export default Contacts;
