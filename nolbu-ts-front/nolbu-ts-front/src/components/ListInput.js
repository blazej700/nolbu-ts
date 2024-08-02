import React from "react";
import { TextInput } from "react95";
import styled from "styled-components";

const Wrapper = styled.div`
  margin: 0.2rem;
`;

export default function ListInput({
  label,
  value,
  onChange,
  register,
  registerName,
}) {
  return (
    <Wrapper>
      <span>{label}</span>
      <TextInput
        value={value}
        onChange={onChange}
        multiline="True"
        rows={8}
        placeholder="Type here..."
        fullWidth
        type="text"
        {...register(registerName)}
      />
    </Wrapper>
  );
}
