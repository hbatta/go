import React from "react";
import * as Yup from "yup";
import { Formik, Field, Form, ErrorMessage } from "formik";
import { GetCSRFToken } from "../../Utils";
import { SingleDatePicker } from "react-dates";
import moment from "moment";
import { FormGroup, Button, Card, CardBody, CardTitle } from "reactstrap";

const DebugCreateYup = Yup.object().shape({
  destination: Yup.string()
    .url()
    .max(1000, "Too Long!"),
  short: Yup.string()
    .required("Required")
    .max(20, "Too Long!"),
  expires: Yup.date()
    .nullable()
    .min(new Date())
});

class DebugCreate extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      focused: false
    };
  }

  render() {
    return (
      <Card>
        <CardBody>
          <CardTitle>Create</CardTitle>
          <Formik
            initialValues={{
              short: "",
              destination: "",
              expires: moment(new Date())
            }}
            validationSchema={DebugCreateYup}
            onSubmit={({ destination, short, expires }, { setSubmitting }) => {
              const newValues = {
                destination: destination,
                short: short,
                date_expires: expires.format()
              };
              fetch("/api/golinks/", {
                method: "post",
                headers: {
                  "Content-Type": "application/json",
                  "X-CSRFToken": GetCSRFToken()
                },
                body: JSON.stringify(newValues)
              })
                .then(response => console.log(response))
                .then(setSubmitting(false));
            }}
            render={({ values, isSubmitting, setFieldValue }) => (
              <Form>
                <FormGroup>
                  {"Destination: "}
                  <Field
                    className="form-control"
                    name="destination"
                    placeholder="https://longwebsitelink.com"
                  />
                  <ErrorMessage name="destination" component="div" />
                </FormGroup>
                <FormGroup>
                  {"Short: "}
                  <Field className="form-control" name="short" />
                  <ErrorMessage name="short" />
                </FormGroup>
                <FormGroup>
                  {"Expires: "}
                  <br />
                  <SingleDatePicker
                    date={values["expires"]} // momentPropTypes.momentObj or null
                    onDateChange={date => setFieldValue("expires", date)} // PropTypes.func.isRequired
                    focused={this.state.focused} // PropTypes.bool
                    onFocusChange={({ focused }) => this.setState({ focused })} // PropTypes.func.isRequired
                    id="expires" // PropTypes.string.isRequired,
                  />
                  <ErrorMessage name="expires" />
                </FormGroup>
                <Button
                  type="submit"
                  disabled={isSubmitting}
                  outline
                  color="primary"
                >
                  Submit
                </Button>
              </Form>
            )}
          />
        </CardBody>
      </Card>
    );
  }
}
export default DebugCreate;